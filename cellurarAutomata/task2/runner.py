import numpy as np
import optparse
from CellularAutomata import CellularAutomata
import matplotlib.pyplot as plt

def get_options():

    optParser = optparse.OptionParser()

    optParser.add_option("-r", dest="radius", help="radius of the cycle", default = 7, type = "int")
    optParser.add_option("-x", dest="X_center", default = 20,
                         help="The X center of the cycle", type = "int")
    optParser.add_option("-y", dest="Y_center", help="The Y center of the cycle", default = 20, type = "int")
    optParser.add_option("-s", dest="size", help="The size of the enviroment", default = 40, type = "int")
    optParser.add_option("-t", dest="time_steps", help="The total number of time steps", default = 6, type = "int")
    optParser.add_option("-n", dest="noise_level", help="The number of cells with noise", default = 1, type = "int")


    options, args = optParser.parse_args()
    return options

def run2(options):

    rows = options.size
    columns = options.size

    enviroments = [CellularAutomata(rows, columns) for i in range(5)]

    for i in enviroments: i.drawCycle(options.radius, options.X_center, options.Y_center)

    enviroments[1].applyNoiseBoundary()
    enviroments[2].applyNoiseBoundary(noiseLevel = options.noise_level)
    enviroments[3].applyNoiseRandom()
    enviroments[4].applyNoiseRandom(noiseLevel = options.noise_level)

    for i in range(options.time_steps):
        print("Time Step: ",i)
        # env.printCA()
        for env in enviroments: env.step(timeStep=i)

    data = [env.getData() for env in enviroments]
    titles = [env.getTitle() for env in enviroments]

    for index, d in enumerate(data):
        plt.plot(d, label=titles[index])
    plt.legend()
    plt.xlabel('Time Step')
    plt.ylabel('Non Zero Elements [Activated Cells]')
    plt.show()

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # run(options)
    run2(options)
