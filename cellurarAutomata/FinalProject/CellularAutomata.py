import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

utilityDecay = 0.97

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

    # def step(self):
