import gym
import matplotlib.pyplot as plt
import numpy as np

stateColor = 0

env = gym.make('BankHeist-v0')
# car  -> rgb(223, 183, 85)
# bank -> rgb(214, 214, 214)
# wall -> rgb(187,187,53)
# free -> rgb(0,0,0)
#         x => [15,147]

# ACTION_MEANING = {
#     0: "NOOP",
#     1: "FIRE",
#     2: "UP",
#     3: "RIGHT",
#     4: "LEFT",
#     5: "DOWN",
#     6: "UPRIGHT",
#     7: "UPLEFT",
#     8: "DOWNRIGHT",
#     9: "DOWNLEFT",
#     10: "UPFIRE",
#     11: "RIGHTFIRE",
#     12: "LEFTFIRE",
#     13: "DOWNFIRE",
#     14: "UPRIGHTFIRE",
#     15: "UPLEFTFIRE",
#     16: "DOWNRIGHTFIRE",
#     17: "DOWNLEFTFIRE",
# }



observation = env.reset()
print(env.observation_space)

# generate mask
wall = observation == np.array([187,187,53])
bank = observation == np.array([214, 214, 214])
# mask = [[ False for _  in range(4)] for _ in range(6) ]
# for x in range(1,3):
#       for y in range(1,5):
#         mask[x][y] = True
#
# for x in range(150):
#     for y in range(200):
#         bonus = False
#         for mX in range(x:x+6):
#             for mY in range(y:y+4):
plt.imshow(wall[:,:,0], cmap='gray')
plt.show()

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
