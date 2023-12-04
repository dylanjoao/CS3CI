
import itertools
import random
import time

import numpy as np


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
                for k in range(len(self.cutting_patterns[i][solution[i][j]])):

                    sum[k] += self.cutting_patterns[i][solution[i][j]][k]

        return sum

    def random_solution(self):
        patterns_used = [] # 2D Array
        satisfied = False

        for i in range(len(self.cutting_patterns)):
            patterns_used.append([])

        while not satisfied:
            r1 = random.randint(0, len(self.cutting_patterns)-1)
            r2 = random.randint(0, len(self.cutting_patterns[r1])-1)
            pattern = self.cutting_patterns[r1][r2]

            patterns_used[r1].append(r2)

            accum_q = self.get_quantities_produced(patterns_used)

            s = True
            for i in range(len(accum_q)):
                if accum_q[i] < self.requested_quantity[i]:
                    s = False
                    break

            if s: 
                satisfied = True

        return patterns_used
    
    def is_valid(self, solution):
        # Check enough quantity is produced 
        # Check the cutting patterns are valid

        valid = True
        accum_q = self.get_quantities_produced(solution)

        for i in range(len(accum_q)):
            if accum_q[i] < self.requested_quantity[i]:
                return False
        

        return valid
 
    def evaluate_cost(self, solution):
    # board * amount of patterns used for board
        cost = [ 0 for i in range(len(solution))]

        for i in range(len(solution)):
            cost[i] += len(solution[i]) * self.available_stock_cost[i]

        return np.sum(cost)
    
    def evaluate_wastage(self, solution):
        wastage = [0 for i in range(len(solution))]

        for i in range(len(solution)):
            for pattern in solution[i]:
                p_i = Pattern(self.cutting_patterns[i][pattern], self.available_lengths[i], self.requested_length)
                wastage[i] += p_i.material_wastage

        return np.sum(wastage)
    
    def view_solution(self, solution):
        patterns = []
        for stock in range(len(solution)):
            stock_patterns = []
            for pattern_index in solution[stock]:
                stock_patterns.append(self.cutting_patterns[stock][pattern_index])
            patterns.append(stock_patterns)
        return patterns


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
def random_search(csp, SOLUTION_FUNC, FITNESS_FUNC, limit):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_solution = []

    # while count < limit:
    while time.time() < end:
        solution = SOLUTION_FUNC()
        fitness = FITNESS_FUNC(solution)

        if (fitness < best_cost):
            best_cost = fitness
            best_solution = solution

        count += 1

    print(f"Best solution after {count} iterations with fitness {best_cost} [Random Search]")
    return best_solution


# # csp = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
# csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])

# random_search_solution = random_search(csp, csp.random_solution, csp.evaluate_cost, 1.0)
# solution = random_search_solution
# patterns = csp.view_solution(solution)
# produced = csp.get_quantities_produced(solution)
# cost = csp.evaluate_cost(solution)
# wastage = csp.evaluate_wastage(solution)
# valid = csp.is_valid(solution)
# print(f"Solution {solution}\nPatterns: {patterns}\nProduced: {produced}\nCost: {cost}\nWastage: {wastage}\nValid: {valid}")