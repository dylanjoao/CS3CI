
import itertools
import random


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
    
class Pattern:
    
    # Pattern [...]
    # of stock length x
    # for requested length y
    def __init__(self, pattern, stock_length, requested_length):
        self.pattern = pattern
        self.stock_length = stock_length
        self.material_wastage = self.calculate_wastage(requested_length)

    def calculate_wastage(self, requested_length):

        total = 0
        for i in range(len(self.pattern)):
            total += self.pattern[i] * requested_length[i]

        return self.stock_length - total

# csp = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])
solution = csp.random_solution()
produced = csp.get_quantities_produced(solution)
print(f"Solution {solution}\nProduced: {produced}")