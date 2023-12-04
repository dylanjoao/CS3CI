import itertools
import random
import pandas as pd
import math
import numpy as np
import time
from itertools import permutations


class CSP:

    # RequestedSize RequestedLength RequestedQuantities AvailSize AvailLengths AvailStockCosts 
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

    def random_solution(self):
        patterns_used = [] # 2D Array
        satisfied = False

        for i in range(len(self.cutting_patterns)):
            patterns_used.append([])

        while not satisfied:
            r1 = random.randint(0, len(self.cutting_patterns)-1)
            r2 = random.randint(0, len(self.cutting_patterns[r1])-1)
            pattern = self.cutting_patterns[r1][r2]

            patterns_used[r1].append(pattern)

            accum_q = self.get_quantities_produced(patterns_used)

            s = True
            for i in range(len(accum_q)):
                if accum_q[i] < self.requested_quantity[i]:
                    s = False
                    break

            if s: 
                satisfied = True

        return patterns_used

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
                    cutting_stock = self.requested_length[k]
                    # 
                    total += value * cutting_stock

                    #
                if total <= self.available_lengths[i] and total > 0:
                    patterns.append(combinations[i][j])

            total_patterns.append(patterns)

        return total_patterns
    
    def get_quantities_produced(self, solution):
        # Returns a 1d array of all quantities produced
        # Sum of all nth element in pattern
        sum = [ 0 for i in range(self.requested_sizes) ]

        #For each stock length pattern
        for i in range(len(solution)):
            stock = solution[i]

            # For each pattern in stock i
            for j in range(len(solution[i])):
                
                # For each value in pattern j
                for k in range(len(solution[i][j])):

                    sum[k] += solution[i][j][k]
                
            

        return sum

    def evaluate_cost(self, solution):
        cost = [ 0 for i in range(len(solution))]

        for i in range(len(solution)):
            cost[i] += len(solution[i]) * self.available_stock_cost[i]

        return cost
    
    def evaluate_wastage(self, solution):
        wastage = [0 for i in range(len(solution))]

        for i in range(len(solution)):
            for pattern in solution[i]:
                p_i = Pattern(pattern, self.available_lengths[i], self.requested_length)
                wastage[i] += p_i.material_wastage

        return wastage

    def is_valid(self, solution):
        # Check enough quantity is produced 
        # Check the cutting patterns are valid
        pass

    def pretty_print_solution(self, solution):
        quantities = self.get_quantities_produced(solution)
        cost_ar = self.evaluate_cost(solution)
        waste = self.evaluate_wastage(solution)
        print(f"Solution: {solution}")
        print(f"Quantities produced: {quantities}, Cost: {cost_ar}, Cost Total: {np.sum(cost_ar)}")
        print(f"Material wastage: {waste}, Wastage Total: {np.sum(waste)}")

class Pattern:

    def __init__(self, pattern, stock_length, requested_length):
        self.pattern = pattern
        self.stock_length = stock_length
        self.material_wastage = self.calculate_wastage(requested_length)

    def calculate_wastage(self, requested_length):

        total = 0
        for i in range(len(self.pattern)):
            total += self.pattern[i] * requested_length[i]

        return self.stock_length - total



# Fitness based on material wastage for now
def random_search(csp, limit):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_solution = []

    # while count < limit:
    while time.time() < end:
        solution = csp.random_solution()
        fitness = np.sum(csp.evaluate_cost(solution))

        if (fitness < best_cost):
            best_cost = fitness
            best_solution = solution

        count += 1

    csp.pretty_print_solution(best_solution)
    print(f"Best solution after {count} iterations with fitness {best_cost} [Random Search]")
    return best_solution

csp_instance = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])
# print(csp_instance.random_solution())
# print(random.sample(csp_instance.cutting_patterns[0], 1))
# print(csp_instance.get_quantities_produced(random.sample(csp_instance.cutting_patterns[0], 1)))
# random_search(csp_instance, 5.0)

# solution = [[(0, 1, 0), (1, 1, 0), (2, 0, 0), (0, 2, 0)], [(1, 1, 1)], [(0, 0, 3), (1, 2, 1)]]
# csp_instance.pretty_print_solution(solution)

# problem_1 = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
# print(random_solution(problem_1))
# print(len(problem_1.cutting_patterns))
# print(random.sample(problem_1.cutting_patterns[0], 1))
# print(problem_1.get_quantities_produced(random.sample(problem_1.cutting_patterns[0], 1)))
# random_search(problem_1, 10.0)

    
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

# RequestedSize RequestedLength RequestedQuantities AvailSize AvailLengths AvailStockCosts 
# Requested Length =    [3, 4, 5, 6, 7, 8, 9, 10]
# Requested Q'ities =   [5, 2, 1, 2, 4, 2, 1, 3]
# Avail Lengths =       [10, 13, 15]

# 3 cutting patterns
# May produce up to 7 pieces for a pattern


    
## Problems
# quantities produced is returning too short of a list