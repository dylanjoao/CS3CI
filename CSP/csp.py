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
        self.requested_quantity = q      # { 5,  7, 5 }

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


csp_instance = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])
# print(csp_instance.bounds)

# for i in range(len(csp_instance.cutting_patterns)):
#     print("\n")
#     for j in range(len(csp_instance.cutting_patterns[i])):
#         print(csp_instance.cutting_patterns[i][j])

def random_search(csp_i):
    patterns_used = [] # 2D Array
    satisfied = False

    for i in range(len(csp_i.cutting_patterns)):
        patterns_used.append([])

    while not satisfied:
        r1 = random.randint(0, len(csp_i.cutting_patterns)-1)
        r2 = random.randint(0, len(csp_i.cutting_patterns[r1])-1)
        pattern = csp_i.cutting_patterns[r1][r2]

        patterns_used[r1].append(pattern)

        accum_q = [ 0 for i in range(len(csp_i.cutting_patterns)) ]

        # For each stock length pattern
        for i in range(len(patterns_used)):

            # For each pattern in stock i
            for j in range(len(patterns_used[i])):

                # For each value in pattern j
                for k in range(len(patterns_used[i][j])):

                    # Add to accum stock column the 
                    accum_q[k] += patterns_used[i][j][k]

        s = True
        for i in range(len(accum_q)):
            if accum_q[i] < csp_i.requested_quantity[i]:
                s = False
                break

        if s: 
            satisfied = True
            print(accum_q)

    print(patterns_used)

    return patterns_used



        
    # print(patterns_used)
    # accum_q = [ 0 for i in range(len(csp_i.cutting_patterns)) ]

    # # For each stock length pattern
    # for i in range(len(patterns_used)):

    #     # For each pattern in stock i
    #     for j in range(len(patterns_used[i])):

    #         # For each value in pattern j
    #         for k in range(len(patterns_used[i][j])):

    #             # Add to accum stock column the 
    #             accum_q[k] += patterns_used[i][j][k]

    # print(accum_q)



random_search(csp_instance)



# requested_q = [5, 7, 5]
# cost = [100, 175, 250]
# satisfied = False

    

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

    
