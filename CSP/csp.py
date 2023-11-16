import itertools
from random import shuffle
import pandas as pd
import math
from itertools import permutations


class CSP:

    def __init__(self, n, rl, q, m, l, c):
        
        self.requested_sizes = n        # 3
        self.requested_length = rl      # { 20, 25, 30 }
        self.requsted_quantity = q      # { 5,  7, 5 }

        self.available_sizes = m        # 3
        self.available_lengths = l      # { 50, 80, 100 }
        self.available_stock_cost = c   # { 100, 175, 250 }
        self.cutting_patterns = []

        # n different sizes                         3
        # rl requested length                       {20,25,30}
        # q quantities of the sizes                 {5,7,5}

        # m amount of stock sizes                   3
        # l lengths of the available stock sizes    {50, 80, 100} 
        # c cost of the stock                       {100, 175, 250}

        # [2, 0, 0]


#####
#
#   If we can generate all possible patterns within the max bounds
#   We can then cull the invalid patterns and be left (all?) valid patterns to select from
#
def generate_bounds(arr_rl, stock_length):

    max_bounds = []
    for i in range(len(arr_rl)):
        max_bounds.append(stock_length // arr_rl[i])

    return max_bounds

def generate_combinations(arr):
    result = []
    length = len(arr)
    patterns = []

    for i in range(length):
        combinations = []
        for j in range(arr[i] + 1):
            combinations.append(j)
        result.append(combinations)

    for combination in itertools.product(*result):
        patterns.append(combination)

    return patterns

def cull_invalid_combinations(combinations, requested_lengths, stock_length):

    patterns = []
    for i in range(len(combinations)):
        total = 0
        for j in range(len(combinations[i])):
            total += combinations[i][j] * requested_lengths[j]

        if total <= stock_length:
            patterns.append(combinations[i])
        print(f"Combination {combinations[i]} = {total} {"YES" if  total <= stock_length else "NO"}")



arl = [20,25,30]
arl_bounds = generate_bounds(arl, 50)
combinations = generate_combinations(arl_bounds)
valid_patterns = cull_invalid_combinations(combinations, arl, 50)



# rl 20 from sl 50
#   2 0 0
#   1 0 0
#   1 1 0
#   0 1 0
#   1 0 1
#   0 0 1
#   0 2 0


### A solution
#
#   Consists of patterns until we are finished 
#   a0  a1  a2  a3  a4  a6 ... Patterns
#   0   1   0   3   0   2       Amount of times used 
#

    
