import gym
import matplotlib.pyplot as plt
import numpy as np

stateColor = 0

# env = gym.make('Freeway-v0')
env = gym.make('MsPacman-v0')
# wall,bonus -> rgb(228,111,111)
# free to move ->  rgb(0,  28, 136)
# pacman -> (210 164  74)

# generate mask
# wall = observation == np.array([228,111,111])
# mask = [[ False for _  in range(4)] for _ in range(6) ]
# for x in range(1,3):
#       for y in range(1,5):
#         mask[x][y] = True


env.reset()
print(env.observation_space)

def diffStates(statePresent, statePast):
    # print(img.shape)
    diff = statePresent - statePast
    # diff[diff!=28] = 0
    x,y = np.nonzero(diff)
    plt.imshow(diff, cmap='gray', vmin=0, vmax=255)
    plt.show()

env.render()
observationPast, reward, done, info = env.step(0) # take a random action

for _ in range(1000):
    env.render()
    observation, reward, done, info = env.step(0) # take a random action
    # print(observation)
    # diffStates(observation-observationPast)
    diffStates(observation[:,:,stateColor],observationPast[:,:,stateColor])
    observationPast = observation
    # diffStates(observation[:,:,1])

env.close()
