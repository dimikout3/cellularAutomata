import numpy as np
import optparse
from CellularAutomata import CellularAutomata
import matplotlib.pyplot as plt
import pdb

def get_options():

    optParser = optparse.OptionParser()

    optParser.add_option("--rI", dest="R_island", help="The radious of the island ",
                         default = 7, type = "int")
    optParser.add_option("--xI", dest="X_island", default = 20,
                         help="The X center of the island", type = "int")
    optParser.add_option("--yI", dest="Y_island", help="The Y center of the island", default = 20, type = "int")
    optParser.add_option("-s", dest="size", help="The size of the enviroment", default = 40, type = "int")
    optParser.add_option("-t", dest="time_steps", help="The total number of time steps", default = 6, type = "int")
    optParser.add_option("--xO", dest="X_oil", default = 15,
                         help="The X coordinate of the oil source", type = "int")
    optParser.add_option("--yO", dest="Y_oil", help="The Y coordinate of the oil source", default = 30, type = "int")

    options, args = optParser.parse_args()
    return options

def getCurrentW2E(size, height, deviation):
    """ Return a simple current from West to East. Height determines where The
    main flow current is located. Deviation how far the current spreads """

    rtnValue = np.zeros([size, size])
    rtnValue[height][:] = 1.0

    map = np.linspace(1,0,deviation+2)

    for i in range(1, deviation+1):
        rtnValue[height + i][:] = map[i]
        rtnValue[height - i][:] = map[i]

    rtnTheta = np.zeros([size, size])

    X = range(size)
    Y = range(size)
    U = rtnValue * np.cos(rtnTheta)
    V = rtnValue * np.sin(rtnTheta)
    # pdb.set_trace()
    color_array = np.sqrt(U)
    plt.quiver(X,Y,U,V,color_array,scale=size)
    plt.colorbar()
    plt.title('Current Spatiotemporal Graph')
    plt.show()
    plt.close()

    return rtnValue, rtnTheta

def getCurrentVοrtice(size):
    """ Return a vortice current """

    rtnValue = np.zeros([size, size])
    rtnTheta = np.zeros([size, size])

    mapIntensity = np.linspace(0,1,size)
    mapTheta = np.linspace(np.pi/2,0,size)

    for i in range(size):
        for j in range(size):
            rtnValue[i][j] = mapIntensity[i]
            rtnTheta[i][j] = mapTheta[j]

    X = range(size)
    Y = range(size)
    U = rtnValue * np.cos(rtnTheta)
    V = rtnValue * np.sin(rtnTheta)
    # pdb.set_trace()
    color_array = np.sqrt(U)
    plt.quiver(X,Y,U,V,color_array,scale=size)
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.title('Current Graph')
    plt.show()
    plt.close()

    return rtnValue, rtnTheta

def run(options):

    rows = options.size
    columns = options.size

    env =  CellularAutomata(rows, columns)

    # currentV, currentT = getCurrentW2E(options.size, 20, 4)
    currentV, currentT = getCurrentVοrtice(options.size)

    env.addIsland(options.R_island, options.X_island, options.Y_island)
    env.addSource(options.X_oil, options.Y_oil)
    env.addCurrent(currentV, currentT)

    for i in range(options.time_steps):
        if (i%15==0):
            env.printCA()
            print("-- Time Step: ",i)
        env.step()


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # run(options)
    run(options)
