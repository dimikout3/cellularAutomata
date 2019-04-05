import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

M = 0.5
d = 0.7
E = 0.01

class CellularAutomata:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.env = np.zeros([rows,columns])
        self.water = (self.env == 0.0)

    def dist(self, x1, y1, x2, y2):
        return math.sqrt( ((x1-x2)**2) + ((y1-y2)**2) )

    def addIsland(self, r, Xcenter, Ycenter):

        for x in range(Xcenter-r, Xcenter+r+1):
            for y in range(Ycenter-r, Ycenter+r+1):
                if self.dist(x, y, Xcenter, Ycenter) < r:
                    self.water[x][y] = False

    def addSource(self, x, y):
        self.X_source = x
        self.Y_source = y
        self.env[x][y] = 1.0

    def printCA(self):
        plt.imshow(self.env, cmap='gray_r')
        # plt.imshow(self.water)
        plt.colorbar()
        plt.show()
        plt.close()

    def saveStep(self, timeStep = None):
        plt.imshow(self.env, cmap='gray')
        plt.colorbar()
        plt.title(self.title+'\nTime Step: '+str(timeStep))
        plt.savefig('results/'+self.title+' Time_Step_'+str(timeStep))
        plt.close()

    def OilMassTranssfer(self, next, r, c):

        ego = self.env[r][c]

        n = self.env[r][c+1] - ego
        nw = self.env[r-1][c+1] - ego
        ne = self.env[r+1][c+1] - ego
        s = self.env[r][c-1] - ego
        sw = self.env[r-1][c-1] - ego
        se = self.env[r+1][c-1] - ego
        w = self.env[r-1][c] - ego
        e = self.env[r+1][c] - ego

        next[r][c] = ego + M*(n + s + w + e) + M*d*(nw + ne + sw + se)

    def Evaporation(self, next, r, c):
        next[r][c] -= next[r][c]*E
        if (next[r][c] <= 0.): next[r][c] = 0.

    def step(self, timeStep = None):

        # self.saveStep(timeStep = timeStep)

        next = np.zeros([self.rows, self.columns])

        for r in range(1, self.rows - 1):
            for c in range(1, self.columns - 1):

                if(self.water[r][c]):
                    self.OilMassTranssfer(next, r, c)
                    # self.Evaporation(next, r, c)

        # self.env = self.env + next
        # self.env[self.env >= 1.] = 1.
        self.env = next
        self.env[self.X_source][self.Y_source] = 1.
        print('Sum = ',np.sum(self.env))
