import itertools
import random
import pandas as pd
import math
import numpy as np
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

        self.bounds = self.generate_bounds()
        combinations = self.generate_combinations()
        self.cutting_patterns = self.cull_invalid_patterns(combinations)

        # n different sizes                         3
        # rl requested length                       {20,25,30}
        # q quantities of the sizes                 {5,7,5}

        # m amount of stock sizes                   3
        # l lengths of the available stock sizes    {50, 80, 100} 
        # c cost of the stock                       {100, 175, 250}

        # [2, 0, 0]

    def generate_bounds(self):
        bounds = []
        for i in range(self.available_sizes):
            max_bounds = []
            for j in range(self.requested_sizes):
                max_bounds.append(self.available_lengths[i] // self.requested_length[j])
            bounds.append(max_bounds)

        return bounds
    

    def generate_combinations(self):

        total_patterns = []

        # For each 
        for i in range(len(self.bounds)):
            result = []
            length = len(self.bounds[i])
            patterns = []

            for j in range(length):
                combinations = []
                for j in range(self.bounds[i][j] + 1):
                    combinations.append(j)
                result.append(combinations)

            for combination in itertools.product(*result):
                patterns.append(combination)

            total_patterns.append(patterns)

        return total_patterns
    
    def cull_invalid_patterns(self, combinations):

        total_patterns = []

        # for each combination
        for i in range(len(combinations)):
            patterns = []

            # for each pattern in combination[i]
            for j in range(len(combinations[i])):
                total = 0

                # for each value in combination[i][j]
                for k in range(len(combinations[i][j])):
                    
                    c_pattern = combinations[i][j]
                    value = combinations[i][j][k]
                    cutting_stock = self.requested_length[i]
                    # 
                    total += value * cutting_stock

                    #
                if total <= self.available_lengths[i]:
                    patterns.append(combinations[i][j])

            total_patterns.append(patterns)

        return total_patterns




#####
#
#   If we can generate all possible patterns within the max bounds
#   We can then cull the invalid patterns and be left (all?) valid patterns to select from
#
#   BELOW IS FOR A SINGLE STOCK LENGTH, NEED TO MODIFY
#
def generate_bounds(requested_length, stock_length):

    max_bounds = []
    for i in range(len(requested_length)):
        max_bounds.append(stock_length // requested_length[i])

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

    return patterns



# arl = [20,25,30]
# arl_bounds = generate_bounds(arl, 50)
# combinations = generate_combinations(arl_bounds)
# valid_patterns = cull_invalid_combinations(combinations, arl, 50)

# # print(arl_bounds)
# for pattern in valid_patterns:
#     print(pattern)
# print("====")

# arl_bounds = generate_bounds(arl, 80)
# combinations = generate_combinations(arl_bounds)
# valid_patterns = cull_invalid_combinations(combinations, arl, 80)
# print(arl_bounds)
# for pattern in valid_patterns:
#     print(pattern)
# print("====")

# arl_bounds = generate_bounds(arl, 100)
# combinations = generate_combinations(arl_bounds)
# valid_patterns = cull_invalid_combinations(combinations, arl, 100)
# print(arl_bounds)
# for pattern in valid_patterns:
#     print(pattern)
# print("====")


csp_instance = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])
print(csp_instance.bounds)

for i in range(len(csp_instance.cutting_patterns)):
    print("\n")
    for j in range(len(csp_instance.cutting_patterns[i])):
        print(csp_instance.cutting_patterns[i][j])

def random_search(csp_i):
    accum_q = np.empty((len(csp_i.cutting_patterns))) # 2d array
    satisfied = False

    while not satisfied:
        r1 = random.randint(0, len(csp_i.cutting_patterns)-1)
        r2 = random.randint(0, len(csp_i.cutting_patterns[r1])-1)
        pattern = csp_i.cutting_patterns[r1][r2]

        np.append(accum_q[r1], pattern)

        print(accum_q)


random_search(csp_instance)



# requested_q = [5, 7, 5]
# cost = [100, 175, 250]
# satisfied = False

# def random_search(valid_pattern, requested_q, cost):
#     accum_q = []
#     selected_patterns = []
#     satisfied = False

#     while not satisfied:
#         sp = random.sample(valid_patterns)
#         selected_patterns.append(sp)
        


#         if ()

    

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

    
