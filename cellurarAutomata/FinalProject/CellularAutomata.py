import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

utilityDecay = 0.9

# car  -> rgb(223, 183, 85)
# bank -> rgb(214, 214, 214)
# wall -> rgb(187,187,53)
# free -> rgb(0,0,0)

MOVE_2_ACTION = {"UP":2,
                 "RIGHT":3,
                 "LEFT":4,
                 "DOWN":5,
                 "UPRIGHT":6,
                 "UPLEFT":7,
                 "DOWNRIGHT":8,
                 "DOWNLEFT":9}

class CellularAutomata:

    def __init__(self, observation):

        self.freeSpace = observation != np.array([187,187,53])
        self.freeSpace[99:140,12,:] = False
        self.freeSpace[99:140,147,:] = False
        # pdb.set_trace()

        self.previousBankLocation = observation == np.array([214, 214, 214])
        # pdb.set_trace()

        (self.rows,self.columns,_) = self.freeSpace.shape

        # oilMass = np.zeros([self.rows, self.columns])
        self.utility = np.zeros([self.rows, self.columns])

        self.updateUtility(self.previousBankLocation[:,:,0])

    def updateUtility(self, banks):

        self.utility[banks==True] = 1.0

        for i in range(90):
            (x,y) = np.where(self.utility>0.)

            for x2,y2 in zip(x,y):

                ego = self.utility[x2][y2]

                utilityValue = ego*utilityDecay

                self.utility[x2][y2+1] = utilityValue if (self.utility[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else self.utility[x2][y2+1]
                self.utility[x2][y2-1] = utilityValue if (self.utility[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else self.utility[x2][y2-1]
                self.utility[x2-1][y2] = utilityValue if (self.utility[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else self.utility[x2-1][y2]
                self.utility[x2+1][y2] = utilityValue if (self.utility[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else self.utility[x2+1][y2]

    def print(self):

        # plt.imshow(self.freeSpace[:,:,0],cmap='gray')
        # plt.imshow(self.previousBankLocation[:,:,0],cmap='gray')
        plt.imshow(self.utility,cmap='gray')

        plt.colorbar()
        plt.show()

    def locateEgoVeh(self, observation):

        egoVeh = observation == np.array([223, 183, 85])
        egoVeh[0:60,:,:]=False

        (x,y) = np.where(egoVeh[:,:,0])

        return x[15],y[15]

    def updatesurroundingUtility(self,x,y):

        surr_utility = {"UP":self.utility[x-1][y],
                        "RIGHT":self.utility[x][y+1],
                        "LEFT":self.utility[x][y-1],
                        "DOWN":self.utility[x+1][y],
                        "UPRIGHT":self.utility[x-1][y+1],
                        "UPLEFT":self.utility[x-1][y-1],
                        "DOWNRIGHT":self.utility[x+1][y+1],
                        "DOWNLEFT":self.utility[x+1][y-1] }

        # print(surr_utility)
        return max(surr_utility,key=surr_utility.get)


    def step(self, observation):

        x,y = self.locateEgoVeh(observation)
        # print('ego veh is located at:',x,y)

        self.currentBankLocation = observation == np.array([214, 214, 214])

        if ( (self.currentBankLocation != self.previousBankLocation).any()):
            self.utility = np.zeros([self.rows, self.columns])
            self.updateUtility(self.currentBankLocation[:,:,0])
            self.previousBankLocation = self.currentBankLocation
            print('Updating bank locations')
            self.print()

        s_utility = self.updatesurroundingUtility(x,y)
        # print(s_utility)

        return MOVE_2_ACTION[s_utility]
