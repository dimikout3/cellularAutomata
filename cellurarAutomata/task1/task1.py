import numpy as np
from math import pow
import matplotlib.pyplot as plt
# np.set_printoptions(threshold=np.inf)

# the radius
global radius

def rule_dictionary(rule_number):
# This function builds a dictionary for any rule from 0 to 255. A cell's neighborhood is its immediate...
# ...neighbors to its left and right——three cells in total. The pattern_list treats the the 2 ** 3 possible...
# ...states as a list. The rule is transformed into assignments of 0s and 1s to the pattern_list...
# ...and builds a dictionary with each possible state as a key.

    pattern_dic = {}
    max_rule = int( pow(2,2*radius + 1) )

    # https://stackoverflow.com/questions/1395356/how-can-i-make-bin30-return-00011110-instead-of-0b11110
    dict_list = [bin(i)[2:].zfill(2*radius + 1) for i in range(max_rule)]
    # https://dbader.org/blog/python-reverse-list
    dict_list.reverse()

    rule_number_binary = bin(rule_number)[2:].zfill(max_rule)

    # build my patterns dictionary
    for indx, val in enumerate(dict_list):
        pattern_dic[val] = rule_number_binary[indx]

    return pattern_dic

def simulation(matrix, pattern_dic):

    rowSize, columnSize = matrix.shape

    for i in range(1,columnSize):
        matrix[i] = step(matrix[i-1], pattern_dic)

    return matrix

def step(previous, pattern_dic):

    nextState = np.zeros(previous.size, dtype=int)
    center = int(previous.size/2)

    for i in range(previous.size):
        key = ''.join(str(x) for x in previous[center-radius:center+radius+1])
        nextState[center] = pattern_dic[key]

        previous = np.roll(previous, 1)
        nextState = np.roll(nextState, 1)

    return nextState

rows = 100
columns = rows
matrix = np.zeros([rows,columns], dtype=int)

# setting initial conditions
_, index = matrix.shape
matrix[0][int(index/2)] = 1

radius = 3

rule = 30                               # Input to the rule_dictionary function.
pattern_dic = rule_dictionary(rule)

matrix = simulation(matrix, pattern_dic)

print(pattern_dic)
# print(matrix)
plt.title("Rule "+str(rule))
plt.imshow(matrix, cmap='binary')
plt.show()
# plt.savefig('Rule_'+str(rule)+'.jpg', bbox_inches="tight")
# plt.close()
