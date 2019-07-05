import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

utilityDecay = 0.975

# car  -> rgb(223, 183, 85)
# bank -> rgb(214, 214, 214)
# wall -> rgb(187,187,53)
# free -> rgb(0,0,0)

WEAKSIDE = 1
STRONGSIDE = 10

MOVE_2_ACTION = {"UP":2,
                 "RIGHT":3,
                 "LEFT":4,
                 "DOWN":5,
                 "UPRIGHT":6,
                 "UPLEFT":7,
                 "DOWNRIGHT":8,
                 "DOWNLEFT":9}

class CellularAutomata:

    def __init__(self, observationEnv):

        self.simStep = 0

        self.observation = observationEnv

        self.freeSpace = self.observation != np.array([187,187,53])
        self.freeSpace[99:140,12,:] = False
        self.freeSpace[99:140,147,:] = False
        # pdb.set_trace()

        self.previousBankLocation = self.observation == np.array([214, 214, 214])
        # pdb.set_trace()

        self.currentBankLocation = self.previousBankLocation

        (self.rows,self.columns,_) = self.freeSpace.shape

        # oilMass = np.zeros([self.rows, self.columns])
        self.utility = np.zeros([self.rows, self.columns])

        self.updateCounter = 0

        # self.updateUtility(self.previousBankLocation[:,:,0])
        self.upadateUtilityDual()


    def positiveUtility(self):
        rtn = np.zeros([self.rows, self.columns])

        rtn[self.currentBankLocation[:,:,0]] = 1.0

        for i in range(90):
            (x,y) = np.where(rtn>0.)

            for x2,y2 in zip(x,y):

                ego = rtn[x2][y2]
                down = rtn[x2+1][y2]
                up = rtn[x2-1][y2]
                right = rtn[x2][y2+1]
                left = rtn[x2][y2-1]

                avgMatrix = np.array([ego,down,left,right,up])
                avgWeights = avgMatrix != 0
                utilityValue = np.average(avgMatrix, weights=avgWeights)*utilityDecay
                # utilityValue = ego*utilityDecay

                rtn[x2][y2+1] = utilityValue if (rtn[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else rtn[x2][y2+1]
                rtn[x2][y2-1] = utilityValue if (rtn[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else rtn[x2][y2-1]
                rtn[x2-1][y2] = utilityValue if (rtn[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else rtn[x2-1][y2]
                rtn[x2+1][y2] = utilityValue if (rtn[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else rtn[x2+1][y2]

        # self.print()
        # plt.imshow(rtn,cmap='gray')
        # plt.colorbar()
        # plt.show()
        return rtn

    def negativeUtility(self):

        rtn = np.zeros([self.rows, self.columns])

        xEgo,yEgo = self.locateEgoVeh()

        rtn[xEgo][yEgo] = 1.0

        for i in range(90):
            (x,y) = np.where(rtn>0.)

            for x2,y2 in zip(x,y):

                ego = rtn[x2][y2]
                down = rtn[x2+1][y2]
                up = rtn[x2-1][y2]
                right = rtn[x2][y2+1]
                left = rtn[x2][y2-1]

                avgMatrix = np.array([ego,down,left,right,up])
                avgWeights = avgMatrix != 0
                utilityValue = np.average(avgMatrix, weights=avgWeights)*utilityDecay
                # utilityValue = ego*utilityDecay

                rtn[x2][y2+1] = utilityValue if (rtn[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else rtn[x2][y2+1]
                rtn[x2][y2-1] = utilityValue if (rtn[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else rtn[x2][y2-1]
                rtn[x2-1][y2] = utilityValue if (rtn[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else rtn[x2-1][y2]
                rtn[x2+1][y2] = utilityValue if (rtn[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else rtn[x2+1][y2]

        return rtn*(-1)

    def upadateUtilityDual(self):

        posUtility = self.positiveUtility()
        negUtility = self.negativeUtility()

        self.utility = posUtility + negUtility
        # self.print()


    def updateUtility(self, banks):

        self.utility[self.previousBankLocation[:,:,0]] = -2.0 - self.updateCounter
        self.utility[banks==True] = 1.0 + self.updateCounter

        for i in range(90):
            (x,y) = np.where(self.utility>0.)

            for x2,y2 in zip(x,y):

                ego = self.utility[x2][y2]
                down = self.utility[x2+1][y2]
                up = self.utility[x2-1][y2]
                right = self.utility[x2][y2+1]
                left = self.utility[x2][y2-1]

                avgMatrix = np.array([ego,down,left,right,up])
                avgWeights = avgMatrix != 0
                utilityValue = np.average(avgMatrix, weights=avgWeights)*utilityDecay
                # utilityValue = ego*utilityDecay

                self.utility[x2][y2+1] = utilityValue if (self.utility[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else self.utility[x2][y2+1]
                self.utility[x2][y2-1] = utilityValue if (self.utility[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else self.utility[x2][y2-1]
                self.utility[x2-1][y2] = utilityValue if (self.utility[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else self.utility[x2-1][y2]
                self.utility[x2+1][y2] = utilityValue if (self.utility[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else self.utility[x2+1][y2]

        self.updateCounter += 10

    def print(self):

        # plt.imshow(self.freeSpace[:,:,0],cmap='gray')
        # plt.imshow(self.previousBankLocation[:,:,0],cmap='gray')
        plt.imshow(self.utility,cmap='gray')

        plt.colorbar()
        plt.show()

    def locateEgoVeh(self):

        egoVeh = self.observation == np.array([223, 183, 85])
        egoVeh[0:60,:,:]=False

        (x,y) = np.where(egoVeh[:,:,0])

        return x[12],y[12]

    def updatesurroundingUtility(self,x,y):

        # pdb.set_trace()

        upMatrix = self.utility[x-STRONGSIDE:x,y-WEAKSIDE:y+WEAKSIDE]
        downMatrix = self.utility[x:x+STRONGSIDE,y-WEAKSIDE:y+WEAKSIDE]
        rightMatrix = self.utility[x-WEAKSIDE:x+WEAKSIDE,y:y+STRONGSIDE]
        leftMatrix = self.utility[x-WEAKSIDE:x+WEAKSIDE,y-STRONGSIDE:y]

        upRightMatrix = self.utility[x-STRONGSIDE:x][y:y+STRONGSIDE]
        upLeftMatrix = self.utility[x-STRONGSIDE:x][y-STRONGSIDE:y]
        downRightMatrix = self.utility[x:x+STRONGSIDE][y:y+STRONGSIDE]
        downLeftMatrxi = self.utility[x:x+STRONGSIDE][y-STRONGSIDE:y]

        surr_utility = {"UP":np.average(upMatrix, weights = upMatrix!= 0.),
                        "RIGHT":np.average(rightMatrix, weights = rightMatrix!= 0.),
                        "LEFT":np.average(leftMatrix, weights = leftMatrix!= 0.),
                        "DOWN":np.average(downMatrix, weights = downMatrix!= 0.)}
                        # "UPRIGHT":np.average(upRightMatrix, weights = upRightMatrix!= 0.),
                        # "UPLEFT":np.average(upLeftMatrix, weights = upLeftMatrix!= 0.),
                        # "DOWNRIGHT":np.average(downRightMatrix, weights = downRightMatrix!= 0.),
                        # "DOWNLEFT":np.average(downLeftMatrxi, weights = downLeftMatrxi!= 0.) }

        print(surr_utility)
        return max(surr_utility,key=surr_utility.get)

    def step(self, observationEnv):

        self.observation = observationEnv

        x,y = self.locateEgoVeh()
        # print('ego veh is located at:',x,y)

        self.currentBankLocation = self.observation == np.array([214, 214, 214])

        if ( (self.currentBankLocation != self.previousBankLocation).any()):
            self.utility = np.zeros([self.rows, self.columns])
            # self.updateUtility(self.currentBankLocation[:,:,0])
            self.upadateUtilityDual()
            self.previousBankLocation = self.currentBankLocation
            print('Updating bank locations')
            self.print()

        s_utility = self.updatesurroundingUtility(x,y)
        print(s_utility)

        self.simStep += 1

        return MOVE_2_ACTION[s_utility]
