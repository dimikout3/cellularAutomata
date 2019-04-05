import numpy as np
import optparse
from CellularAutomata import CellularAutomata
import matplotlib.pyplot as plt

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

def run(options):

    rows = options.size
    columns = options.size

    env =  CellularAutomata(rows, columns)

    env.addIsland(options.R_island, options.X_island, options.Y_island)
    env.addSource(options.X_oil, options.Y_oil)

    for i in range(options.time_steps):
        print("Time Step: ",i)
        if (i%20==0): env.printCA()
        env.step()


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # run(options)
    run(options)
