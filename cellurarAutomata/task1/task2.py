import numpy as np
from math import pow
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as mpatches
import itertools
# np.set_printoptions(threshold=np.inf)

# the radius
global radius
global ruleSize

def rule_dictionary(rule, distinct):

    # distinctList = ['0', '1', '2', ... 'distinct-1']
    distinctList = [str(i) for i in range(distinct)]

    # perm = [('0,'0','0'), ('0','0','1'), ... ('2', '2', '2')]
    perm = [i for i in itertools.product(distinctList, repeat=(2*radius+1))]

    # keys = ['000', '001', ... '222']
    keys = [''.join(i) for i in perm]

    pattern_dic = {}

    for indx, val in enumerate(keys):
        pattern_dic[val] = rule[indx]

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

# number of distinct values (binary = 2)
distinct = 3

# number of left and right cells (default = 1)
radius = 1

examples = 10
distinctList = [3, 4, 5, 6]
radList = [1, 2, 3]

for distinct in distinctList:
    for rad in radList:
        radius = rad

        for example in range(examples):

            rows = 100
            columns = rows
            matrix = np.zeros([rows,columns], dtype=int)

            # setting initial conditions (random)
            matrix[0] = np.random.randint(distinct, size = columns)

            ruleSize = int( pow(distinct, 2*radius + 1) )
            rule = [str( np.random.randint(distinct) ) for i in range(ruleSize) ]
            # Input to the rule_dictionary function.
            pattern_dic = rule_dictionary(rule, distinct)

            matrix = simulation(matrix, pattern_dic)

            print('\nClasses :',distinct, ' Radius :',radius, ' Example :',example)
            print('Lookup table :',pattern_dic)
            # print(matrix)
            # plt.title("Rule "+str(''.join(rule[:27]))+'\n'+str(''.join(rule[27:])))
            plt.title('Classes :'+str(distinct)+' Radius :'+str(radius))
            colorBar = cm.jet
            im = plt.imshow(matrix, colorBar)

            values = np.unique(matrix.ravel())
            colors = [ im.cmap(im.norm(value)) for value in values]
            # create a patch (proxy artist) for every color
            patches = [ mpatches.Patch(color=colors[i], label="Class {l}".format(l=values[i]) ) for i in range(len(values)) ]
            # put those patched as legend-handles into the legend
            plt.legend(handles=patches, bbox_to_anchor=(1.0, 1.0), loc=2)

            # plt.show()
            plt.savefig('Mul/Classes_'+str(distinct)+'_Radius_'+str(radius)+'_Example_'+str(example)+'.jpg', bbox_inches="tight")
            plt.close()
