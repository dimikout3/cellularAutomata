import gym
import numpy as np
import optparse
from CellularAutomata import CellularAutomata
import matplotlib.pyplot as plt
import pdb
import time

def get_options():

    optParser = optparse.OptionParser()

    optParser.add_option("--rI", dest="R_island", help="The radious of the island ",
                         default = 7, type = "int")
    optParser.add_option("--xI", dest="X_island", default = 20,
                         help="The X center of the island", type = "int")
    optParser.add_option("--yI", dest="Y_island", help="The Y center of the island", default = 20, type = "int")
    optParser.add_option("-s", dest="size", help="The size of the enviroment", default = 40, type = "int")
    optParser.add_option("-t", dest="time_steps", help="The total number of time steps", default = 15, type = "int")
    optParser.add_option("--xO", dest="X_oil", default = 15,
                         help="The X coordinate of the oil source", type = "int")
    optParser.add_option("--yO", dest="Y_oil", help="The Y coordinate of the oil source", default = 30, type = "int")

    options, args = optParser.parse_args()
    return options

def run(options):

    #initiate enviroment
    atari = gym.make('BankHeist-v0')

    observation = atari.reset()

    # initiate class
    envCA =  CellularAutomata(observation)


    for i in range(options.time_steps):
        atari.render()

        action = envCA.step(observation)

        observation, reward, done, info = atari.step(action) # take a random action
        time.sleep(0.1)
        # pdb.set_trace()

        # envCA.print()

    atari.close()

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # run(options)
    run(options)
