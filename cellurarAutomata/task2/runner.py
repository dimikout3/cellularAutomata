import numpy as np
import optparse
from CellularAutomata import CellularAutomata

def get_options():

    optParser = optparse.OptionParser()

    optParser.add_option("-r", dest="radius", help="radius of the cycle", default = 5, type = "int")
    optParser.add_option("-x", dest="X_center", default = 20,
                         help="The X center of the cycle", type = "int")
    optParser.add_option("-y", dest="Y_center", help="The Y center of the cycle", default = 20, type = "int")
    optParser.add_option("-s", dest="size", help="The size of the enviroment", default = 40, type = "int")


    options, args = optParser.parse_args()
    return options

def run2(options):

    rows = options.size
    columns = options.size

    env = CellularAutomata(rows, columns)

    env.drawCycle(options.radius, options.X_center, options.Y_center)
    env.applyNoiseBoundary()
    # env.printCA()
    for i in range(6):
        env.printCA()
        env.step()

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # run(options)
    run2(options)
