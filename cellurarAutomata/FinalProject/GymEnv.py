import gym
import matplotlib.pyplot as plt
import numpy as np

stateColor = 1

env = gym.make('Freeway-v0')
env.reset()
print(env.observation_space)

def diffStates(statePresent, statePast):
    # print(img.shape)
    diff = statePresent - statePast
    x,y = np.nonzero(diff)
    plt.imshow(diff)
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
