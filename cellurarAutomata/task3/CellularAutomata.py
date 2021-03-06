import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

M = 0.1
d = 0.7
E = 0.01

class CellularAutomata:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.env = np.zeros([rows,columns])
        self.water = (self.env == 0.0)
        self.title = 'Oil Slick'
        self.rI = 0

    def dist(self, x1, y1, x2, y2):
        return math.sqrt( ((x1-x2)**2) + ((y1-y2)**2) )

    def addIsland(self, r, Xcenter, Ycenter):

        self.xI = Xcenter
        self.yI = Ycenter
        self.rI = r

        for x in range(Xcenter-r, Xcenter+r+1):
            for y in range(Ycenter-r, Ycenter+r+1):
                if self.dist(x, y, Xcenter, Ycenter) < r:
                    self.water[x][y] = False

    def addSource(self, x, y):
        self.X_source = x
        self.Y_source = y
        self.env[x][y] = 1.0

    def addCurrent(self, V, T):

        self.current = [[{} for j in range(self.columns)] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                self.current[i][j]['N'] = V[i][j]*np.sin(T[i][j])
                self.current[i][j]['S'] = -V[i][j]*np.sin(T[i][j])
                self.current[i][j]['W'] = -V[i][j]*np.cos(T[i][j])
                self.current[i][j]['E'] = V[i][j]*np.cos(T[i][j])
                self.current[i][j]['NE'] = V[i][j]*np.sin(np.pi/4 + T[i][j])
                self.current[i][j]['NW'] = -V[i][j]*np.cos(T[i][j] - np.pi/4)
                self.current[i][j]['SE'] = V[i][j]*np.cos(T[i][j] - np.pi/4)
                self.current[i][j]['SW'] = -V[i][j]*np.sin(np.pi/4 + T[i][j])

    def printCA(self, step=None):

        cmapSea = plt.cm.get_cmap('bone_r',100)
        cmapTerain = plt.cm.get_cmap('pink',self.rI)

        image = [[j for j in range(self.columns)] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                if self.water[i][j]:
                    image[i][j] = cmapSea(self.env[i][j])
                else:
                    d = self.dist(i, j, self.xI, self.yI)
                    indx = 1/d if d!=0 else 0.
                    image[i][j] = cmapTerain(indx)

        plt.imshow(image, cmap=cmapSea)
        # plt.imshow(self.water)
        plt.colorbar()

        if set != None:
            plt.title(self.title + '- Time Step : '+str(step))
        else:
            plt.title(self.title)

        plt.xlabel('X - Axis')
        plt.ylabel('Y - Axis')
        plt.show()
        plt.close()

    def saveStep(self, step = None):

        cmapSea = plt.cm.get_cmap('bone_r',100)
        cmapTerain = plt.cm.get_cmap('pink',self.rI)

        image = [[j for j in range(self.columns)] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                if self.water[i][j]:
                    image[i][j] = cmapSea(self.env[i][j])
                else:
                    d = self.dist(i, j, self.xI, self.yI)
                    indx = 1/d if d!=0 else 0.
                    image[i][j] = cmapTerain(indx)

        # plt.imshow(image, cmap=cmapSea, interpolation='bilinear')
        plt.imshow(image, cmap=cmapSea)
        # plt.imshow(self.water)
        plt.colorbar()

        if set != None:
            plt.title(self.title + '- Time Step : '+str(step))
        else:
            plt.title(self.title)

        plt.xlabel('X - Axis')
        plt.ylabel('Y - Axis')

        plt.savefig('results/'+self.title+' Time Step '+str(step))
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

    def Current(self, next, r, c):

        ego = self.env[r][c]

        n = (self.env[r-1][c] - ego)*self.current[r][c]['S']
        nw = (self.env[r-1][c-1] - ego)*self.current[r][c]['SE']
        ne = (self.env[r-1][c+1] - ego)*self.current[r][c]['SW']
        s = (self.env[r+1][c] - ego)*self.current[r][c]['N']
        sw = (self.env[r+1][c-1] - ego)*self.current[r][c]['NE']
        se = (self.env[r+1][c+1] - ego)*self.current[r][c]['NW']
        w = (self.env[r][c-1] - ego)*self.current[r][c]['E']
        e = (self.env[r][c+1] - ego)*self.current[r][c]['W']

        next[r][c] = M*(n + s + w + e) + M*d*(nw + ne + sw + se)

    def Evaporation(self, next, r, c):
        next[r][c] -= next[r][c]*E
        if (next[r][c] <= 0.): next[r][c] = 0.

    def step(self, step = None):

        if (step % 5 == 0) :self.saveStep(step = step)

        oilMass = np.zeros([self.rows, self.columns])
        evapor = np.zeros([self.rows, self.columns])
        curr = np.zeros([self.rows, self.columns])

        for r in range(1, self.rows - 1):
            for c in range(1, self.columns - 1):

                if(self.water[r][c]):
                    self.OilMassTranssfer(oilMass, r, c)
                    self.Evaporation(evapor, r, c)
                    self.Current(curr, r, c)

        self.env = self.env*0.1 + oilMass + evapor + curr
        self.env[self.env >= 1.] = 1.
        # self.env = next
        self.env[self.X_source][self.Y_source] = 1.
        # count_nonzero
        # print('Non Zero Elements  = ',np.count_nonzero(self.env))
        # print('Sum = ',np.sum(self.env))
