import numpy as np
import math
import matplotlib.pyplot as plt
import pdb
import time
import os

plt.style.use('seaborn')

UTILITYDECAY = 0.97
POLICE_DECAY = 0.95

CLEAR_RANGE = 1
POLICE_RANGE = 40
BANK_RANGE = 90

UPDATEMOD = 5
DIST = 30

UPDATE_INTERVAL_BANK = 15
UPDATE_INTERVAL_POLICE = 5

# car  -> rgb(223, 183, 85)
# bank -> rgb(214, 214, 214)
# wall -> rgb(187,187,53)
# free -> rgb(0,0,0)
# police -> rgb(24,26,167)

WEAKSIDE = 2
STRONGSIDE = 8

VERBOSE = True
INFO = True
SIM = True
DEBUG = False
RECORD = True
RECORD_INTERVAL = 5

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

        self.updateUtilityPoliceVeh()

        self.updateUtilityBanks()

        self.aggregateUtility()

        self.updateStepBank = UPDATE_INTERVAL_BANK
        self.updateStepPolice = UPDATE_INTERVAL_POLICE

        self.printFullEnv()

        # self.updateUtility(self.previousBankLocation[:,:,0])
        # self.updateUtilityMulti()


    def distance(self, x, y, xList, yList):

        dList =[]
        for xl,yl in zip(xList,yList):

            d = math.sqrt( ((x-xl)**2) + ((y-yl)**2) )
            dList.append(d)

        return min(dList) if dList != [] else 0


    def updateUtilityPoliceVeh(self):
        if VERBOSE and INFO:
            print('[INFO]: updating utility for police veh')

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
                # utilityValue = np.average(avgMatrix, weights=avgWeights)*POLICE_DECAY*(((POLICE_RANGE-i)/POLICE_RANGE)**2)
                utilityValue = np.average(avgMatrix, weights=avgWeights)*POLICE_DECAY
                # utilityValue = ego*UTILITYDECAY

                rtn[x2][y2+1] = utilityValue if (rtn[x2][y2+1]==0. and self.freeSpace[x2][y2+1][0] ) else rtn[x2][y2+1]
                rtn[x2][y2-1] = utilityValue if (rtn[x2][y2-1]==0. and self.freeSpace[x2][y2-1][0] ) else rtn[x2][y2-1]
                rtn[x2-1][y2] = utilityValue if (rtn[x2-1][y2]==0. and self.freeSpace[x2-1][y2][0] ) else rtn[x2-1][y2]
                rtn[x2+1][y2] = utilityValue if (rtn[x2+1][y2]==0. and self.freeSpace[x2+1][y2][0] ) else rtn[x2+1][y2]

        self.utilityPoliceVeh = rtn*(-1)


    def clearBankNoise(self, rtn):

        if VERBOSE and INFO:
            print('[INFO]: clearing noise banks')

        toZero = []

        for i in range(CLEAR_RANGE):
            (x,y) = np.where(rtn>0.)

            for x2,y2 in zip(x,y):

                down = (rtn[x2+1][y2] == 0)
                up = (rtn[x2-1][y2] == 0)
                right = (rtn[x2][y2+1] == 0)
                left = (rtn[x2][y2-1] == 0)

                if down or up or right or left:
                    toZero.append([x2,y2])

            for x0,y0 in toZero:
                rtn[x0][y0] = 0.

        return rtn


    def boundaries(self, rtn):

        r1 = np.roll(rtn,1,axis=0)
        r2 = np.roll(rtn,-1,axis=0)
        r3 = np.roll(rtn,1,axis=1)
        r4 = np.roll(rtn,-1,axis=1)

        xor1 = np.logical_and( np.logical_xor(r1, rtn) , self.freeSpace[:,:,0])
        xor2 = np.logical_and( np.logical_xor(r2, rtn) , self.freeSpace[:,:,0])
        xor3 = np.logical_and( np.logical_xor(r3, rtn) , self.freeSpace[:,:,0])
        xor4 = np.logical_and( np.logical_xor(r4, rtn) , self.freeSpace[:,:,0])

        bound = np.logical_or( np.logical_or(xor1,xor2), np.logical_or(xor3,xor4))

        return np.where(bound)

    def updateUtilityBanks(self):

        if VERBOSE and INFO:
            print('[INFO]: updating utility for banks')

        rtn = np.zeros([self.rows, self.columns])

        rtn[self.currentBankLocation[:,:,0]] = 1.0

        rtn = self.clearBankNoise(rtn)

        for i in range(BANK_RANGE):
            (x,y) = self.boundaries(rtn)

            for x2,y2 in zip(x,y):

                down = rtn[x2+1][y2]
                up = rtn[x2-1][y2]
                right = rtn[x2][y2+1]
                left = rtn[x2][y2-1]

                avgMatrix = np.array([down,left,right,up])
                avgWeights = avgMatrix != 0
                utilityValue = np.average(avgMatrix, weights=avgWeights)*UTILITYDECAY

                rtn[x2][y2] = utilityValue

            self.printSingle(rtn,'Utility Banks {} [step]'.format(i),i)
        self.utilityBanks = rtn


    def aggregateUtility(self):

        if VERBOSE and INFO:
            print('[INFO]: Aggregating utilities ...')

        self.utility = self.utilityBanks + self.utilityPoliceVeh


    def printSingle(self, img=[], title='No Title Given', ustep=0):

        plt.imshow(img,cmap='jet',vmin=-1,vmax=1)
        plt.title(title)
        cbr = plt.colorbar()
        cbr.set_label('Utility')

        plt.grid(False)

        if DEBUG:
            plt.show()
        elif RECORD:
            plt.savefig('results/utility'+str(ustep)+'.png')
        else:
            plt.show(block=False)
            plt.pause(3)

        plt.close()

    def printFullEnv(self):

        # plt.imshow(self.freeSpace[:,:,0],cmap='gray')
        # plt.imshow(self.previousBankLocation[:,:,0],cmap='gray')
        defaultAspect = 1
        ig, ax = plt.subplots(nrows=2, ncols=2)

        ax[0,0].imshow(self.observation, aspect = defaultAspect)
        ax[0,0].set_title('Enviroment: {}[s]'.format(self.simStep))
        ax[0,0].grid(False)

        ax[0,1].imshow(self.utilityPoliceVeh, aspect = defaultAspect,
        cmap='jet', vmin=-1, vmax=1)
        ax[0,1].set_title('Utility of Police Veh')
        ax[0,1].grid(False)

        ax[1,0].imshow(self.utilityBanks, aspect = defaultAspect,
        cmap='jet', vmin=-1, vmax=1)
        ax[1,0].set_title('Utility of Banks')
        ax[1,0].grid(False)

        ax[1,1].imshow(self.utility, aspect = defaultAspect,
        cmap='jet', vmin=-1, vmax=1)
        ax[1,1].set_title('Aggregated Utility')
        ax[1,1].grid(False)

        plt.tight_layout()

        if not os.path.exists("results"):
            os.mkdir("results")

        if DEBUG:
            plt.show()
        elif RECORD:
            plt.savefig('results/'+str(self.simStep)+'.png')
        else:
            plt.show(block=False)
            plt.pause(3)

        plt.close()


    def locateEgoVeh(self):

        egoVeh = self.observation == np.array([223, 183, 85])
        egoVeh[0:60,:,:]=False

        (x,y) = np.where(egoVeh[:,:,0])

        xInt = int(np.average(x))
        yInt = int(np.average(y))

        return xInt,yInt


    def locatePoliceVeh(self):

        policeVeh = self.observation == np.array([24,26,167])
        policeVeh[0:60,:,:]=False

        (x,y) = np.where(policeVeh[:,:,0])

        return x,y


    def updatesurroundingUtility(self,x,y):

        upMatrix = self.utility[x-STRONGSIDE:x,y-WEAKSIDE:y+WEAKSIDE]
        downMatrix = self.utility[x:x+STRONGSIDE,y-WEAKSIDE:y+WEAKSIDE]
        rightMatrix = self.utility[x-WEAKSIDE:x+WEAKSIDE,y:y+STRONGSIDE]
        leftMatrix = self.utility[x-WEAKSIDE:x+WEAKSIDE,y-STRONGSIDE:y]

        surr_utility = {"RIGHT":np.sum(rightMatrix)/(STRONGSIDE*WEAKSIDE),
                        "UP":np.sum(upMatrix)/(STRONGSIDE*WEAKSIDE),
                        "LEFT":np.sum(leftMatrix)/(STRONGSIDE*WEAKSIDE),
                        "DOWN":np.sum(downMatrix)/(STRONGSIDE*WEAKSIDE)}

        if VERBOSE and SIM:
            print('[SIM]: surrounding utility dict',surr_utility)

        return max(surr_utility,key=surr_utility.get)


    def step(self, observationEnv):

        start_time = time.time()

        if VERBOSE:print('\n-------- sim step: ',self.simStep)

        self.observation = observationEnv

        x,y = self.locateEgoVeh()
        # print('ego veh is located at:',x,y)

        self.currentBankLocation = self.observation == np.array([214, 214, 214])
        self.currentPoliceLocation = self.observation == np.array([24,26,167])

        # updateStepBanks = (self.simStep%UPDATEMOD == 0)
        # updateStepPolice =

        if (self.currentBankLocation != self.previousBankLocation).any() and (self.updateStepBank <= self.simStep):

            if VERBOSE and SIM:
                print('[SIM]: Difference in Bank Locations')

            self.utility = np.zeros([self.rows, self.columns])

            self.updateUtilityBanks()
            self.aggregateUtility()

            self.previousBankLocation = self.currentBankLocation
            self.updateStepBank = self.simStep + UPDATE_INTERVAL_BANK

            self.printFullEnv()

        if (self.currentPoliceLocation != self.previousPoliceLocation).any() and (self.updateStepPolice <= self.simStep):

            xPolice, yPolice = self.locatePoliceVeh()
            dist = self.distance(x,y,xPolice, yPolice)

            if dist<DIST:

                if VERBOSE and SIM:
                    print('[SIM]: Difference in Police Car Locations')

                self.utility = np.zeros([self.rows, self.columns])

                self.updateUtilityPoliceVeh()
                self.aggregateUtility()

                self.previousPoliceLocation = self.currentPoliceLocation
                self.updateStepPolice = self.simStep + UPDATE_INTERVAL_POLICE

                self.printFullEnv()

        s_utility = self.updatesurroundingUtility(x,y)

        updateRecord = self.simStep%RECORD_INTERVAL == 0
        if RECORD and updateRecord:
            self.printFullEnv()

        if VERBOSE and SIM:
            print('[SIM]: Next action is',s_utility)

        self.simStep += 1

        elapsed_time = time.time() - start_time

        if VERBOSE and SIM:
            print('[SIM]: Simulation step elapsed after {} [sec]'.format(elapsed_time))

        return MOVE_2_ACTION[s_utility]
