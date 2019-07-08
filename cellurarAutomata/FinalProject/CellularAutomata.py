import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

utilityDecay = 0.975

NEGATIVE_VEH_DECAY = 0.87

POLICE_DECAY = 0.8

VEH_RANGE = 40
POLICE_RANGE = 30
BANK_RANGE = 90

# car  -> rgb(223, 183, 85)
# bank -> rgb(214, 214, 214)
# wall -> rgb(187,187,53)
# free -> rgb(0,0,0)
# police -> rgb(24,26,167)

WEAKSIDE = 1
STRONGSIDE = 10

VERBOSE = True
INFO = True
SIM = True

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

        self.previousBankLocation = self.observation == np.array([214, 214, 214])
        self.currentBankLocation = self.previousBankLocation

        self.previousPoliceLocation = self.observation == np.array([24,26,167])
        self.currentPoliceLocation = self.previousPoliceLocation

        (self.rows,self.columns,_) = self.freeSpace.shape

        # oilMass = np.zeros([self.rows, self.columns])
        self.utility = np.zeros([self.rows, self.columns])

        self.updateCounter = 0

        # self.updateUtility(self.previousBankLocation[:,:,0])
        self.updateUtilityMulti()


    def distance(self, x, y, x2, y2):

        d = math.sqrt( ((x-x2)**2) + ((y-y2)**2) )

        if d<1:d = 1

        return d


    def positiveUtility(self):

        if VERBOSE and INFO:
            print('[INFO]: calculating positive utility for banks')

        rtn = np.zeros([self.rows, self.columns])

        rtn[self.currentBankLocation[:,:,0]] = 1.0

        for i in range(BANK_RANGE):
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


    def negativeUtilityVeh(self):

        if VERBOSE and INFO:
            print('[INFO]: calculating negative utility for ego veh')

        rtn = np.zeros([self.rows, self.columns])

        xEgo,yEgo = self.locateEgoVeh()

        rtn[xEgo][yEgo] = 2.0

        for i in range(VEH_RANGE):
            (x,y) = np.where(rtn>0.)

            for x2,y2 in zip(x,y):

                ego = rtn[x2][y2]
                down = rtn[x2+1][y2]
                up = rtn[x2-1][y2]
                right = rtn[x2][y2+1]
                left = rtn[x2][y2-1]

                avgMatrix = np.array([ego,down,left,right,up])
                avgWeights = avgMatrix != 0
                # dist = self.distance(xEgo, yEgo, x2, y2)
                utilityValue = np.average(avgMatrix, weights=avgWeights)*NEGATIVE_VEH_DECAY
                # utilityValue = ego*utilityDecay

                rtn[x2][y2+1] = utilityValue if (rtn[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else rtn[x2][y2+1]
                rtn[x2][y2-1] = utilityValue if (rtn[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else rtn[x2][y2-1]
                rtn[x2-1][y2] = utilityValue if (rtn[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else rtn[x2-1][y2]
                rtn[x2+1][y2] = utilityValue if (rtn[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else rtn[x2+1][y2]

        return rtn*(-1)


    def negativeUtilityPol(self):

        if VERBOSE and INFO:
            print('[INFO]: calculating negative police utility')

        rtn = np.zeros([self.rows, self.columns])

        rtn[self.currentPoliceLocation[:,:,0]] = 1.0

        for i in range(POLICE_RANGE):
            (x,y) = np.where(rtn>0.)

            for x2,y2 in zip(x,y):

                ego = rtn[x2][y2]
                down = rtn[x2+1][y2]
                up = rtn[x2-1][y2]
                right = rtn[x2][y2+1]
                left = rtn[x2][y2-1]

                avgMatrix = np.array([ego,down,left,right,up])
                avgWeights = avgMatrix != 0
                utilityValue = np.average(avgMatrix, weights=avgWeights)*POLICE_DECAY
                # utilityValue = ego*utilityDecay

                rtn[x2][y2+1] = utilityValue if (rtn[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else rtn[x2][y2+1]
                rtn[x2][y2-1] = utilityValue if (rtn[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else rtn[x2][y2-1]
                rtn[x2-1][y2] = utilityValue if (rtn[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else rtn[x2-1][y2]
                rtn[x2+1][y2] = utilityValue if (rtn[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else rtn[x2+1][y2]

        return rtn*(-1)


    def updateUtilityMulti(self):

        if VERBOSE and INFO:
            print('[INFO]: updating utility ...')

        posUtility = self.positiveUtility()
        negVehUtility = self.negativeUtilityVeh()
        negPoliceUtily = self.negativeUtilityPol()

        self.utility = posUtility + negVehUtility + negPoliceUtily
        self.print(self.utility)


    def print(self,img):

        # plt.imshow(self.freeSpace[:,:,0],cmap='gray')
        # plt.imshow(self.previousBankLocation[:,:,0],cmap='gray')
        plt.imshow(img,cmap='gray')
        plt.colorbar()
        plt.show()
        plt.close()


    def locateEgoVeh(self):

        egoVeh = self.observation == np.array([223, 183, 85])
        egoVeh[0:60,:,:]=False

        (x,y) = np.where(egoVeh[:,:,0])

        return x[10],y[10]


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

        if VERBOSE and SIM:
            print('[SIM]: surrounding utility dict',surr_utility)

        return max(surr_utility,key=surr_utility.get)


    def step(self, observationEnv):

        if VERBOSE:print('\n-------- sim step: ',self.simStep)

        self.observation = observationEnv

        x,y = self.locateEgoVeh()
        # print('ego veh is located at:',x,y)

        self.currentBankLocation = self.observation == np.array([214, 214, 214])
        self.currentPoliceLocation = self.observation == np.array([24,26,167])

        updateStep = (self.simStep%5 == 0)

        if (self.currentBankLocation != self.previousBankLocation).any() and (updateStep):

            if VERBOSE and SIM:
                print('[SIM]: Difference in Bank Locations')

            self.utility = np.zeros([self.rows, self.columns])

            self.updateUtilityMulti()
            self.previousBankLocation = self.currentBankLocation

        elif (self.currentPoliceLocation != self.previousPoliceLocation).any() and (updateStep):

            if VERBOSE and SIM:
                print('[SIM]: Difference in Police Car Locations')

            self.utility = np.zeros([self.rows, self.columns])

            self.updateUtilityMulti()
            self.previousPoliceLocation = self.currentPoliceLocation



        s_utility = self.updatesurroundingUtility(x,y)

        if VERBOSE and SIM:
            print('[SIM]: Next action is',s_utility)

        self.simStep += 1

        return MOVE_2_ACTION[s_utility]
