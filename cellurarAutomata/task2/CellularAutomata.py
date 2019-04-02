import numpy as np
import math
import matplotlib.pyplot as plt
import pdb

class CellularAutomata:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.env = np.ones([rows,columns])

    def dist(self, x1, y1, x2, y2):
        return math.sqrt( ((x1-x2)**2) + ((y1-y2)**2) )

    def drawCycle(self, r, Xcenter, Ycenter):

        self.r = r
        self.Xcenter = Xcenter
        self.Ycenter = Ycenter

        for x in range(Xcenter-r, Xcenter+r+1):
            for y in range(Ycenter-r, Ycenter+r+1):
                if self.dist(x, y, Xcenter, Ycenter) < r:
                    self.env[x][y] = 0

    def printCA(self):
        plt.imshow(self.env)
        plt.colorbar()
        plt.show()
        plt.close()

    def applyNoiseBoundary(self, noiseLevel = 1):

        (rows, columns) = np.where(self.env == 0)

        boundaries = []

        for (r, c) in zip(rows, columns):

            north = self.env[r+1][c] == 1
            south = self.env[r-1][c] == 1
            west = self.env[r][c-1] == 1
            east = self.env[r][c+1] == 1
            ego = self.env[r][c] == 0

            if ( (north or south or west or east) and ego):
                boundaries.append([r, c])

        noiseIndexes = np.random.choice(range(len(boundaries)), noiseLevel, replace=False)

        for i in noiseIndexes:
            # print('boundaries are :',boundaries[i][0],boundaries[i][1])
            self.env[ boundaries[i][0] ][ boundaries[i][1]] = 1


    def applyNoiseRandom(self, noiseLevel = 1):

        (rows, columns) = np.where(self.env == 0)
        # pdb.set_trace()

        while (noiseLevel>0):
            randIndx = np.random.randint(len(rows))
            if self.dist(rows[randIndx], columns[randIndx], self.Xcenter, self.Ycenter) < (self.r - 1):
                self.env[ rows[randIndx] ][ columns[randIndx] ] = 1
                noiseLevel -= 1

    def step(self):

        (rows, columns) = np.where(self.env == 0)

        next = np.zeros([self.rows, self.columns])

        for (r, c) in zip(rows, columns):

            north = self.env[r+1][c] == 1
            south = self.env[r-1][c] == 1
            west = self.env[r][c-1] == 1
            east = self.env[r][c+1] == 1
            ego = self.env[r][c] == 1

            if (north or south or west or east or ego):
                # self.env[r][c] = 1
                next[r][c] = 1
        self.env = self.env + next
