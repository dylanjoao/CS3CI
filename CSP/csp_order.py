
class CSP:

    # Solution representation
    # Order request:    5  4  6  3  3  4  6  6  
    # Cutting points:  | 12 |   12    | 12 | 12 |
    # Wastage:            3      0       2    6  
    #
    # A solution is the order of the order request list
    # It is then decoded to find the cutting points 
    # The decoded will always return the same result


    def __init__(self, n, rl, q, m, l, c):
        
        self.requested_unique_amount = n       # 3
        self.requested_length = rl      # { 20, 25, 30 }
        self.requested_quantity = q     # { 5,  7, 5 }

        self.stock_n = m                # 3
        self.stock_lengths = l          # { 50, 80, 100 }
        self.stock_costs = c            # { 100, 175, 250 }

    # 5  4  6  3  3  4  6  6  
    # return cutting points
    def decode(self, solution):
        points = []
        total_wastage = 0
        total_cost = 0

        index = 0
        done = False

        while not done:

            # Accumulate the amounts under the stock lengths
            accum = []
            accum_count = [0 for i in range(self.stock_n)]
            for i in range(self.stock_n):
                total = 0
                # For each value in solution
                for j in range(index, len(solution)):
                    # If total goes over stock length stop
                    if total + solution[j] > self.stock_lengths[i]: break
                    # Else add to total
                    total += solution[j]
                    accum_count[i] += 1

                accum.append(total)
            
            # Choose best option based on wastage
            best_wastage = float('inf')
            best_stock_index = None
            for i in range(self.stock_n):
                wastage = self.stock_lengths[i] - accum[i]
                if wastage < best_wastage:
                    best_wastage = wastage
                    best_stock_index = i
            
            points.append((index+accum_count[best_stock_index], self.stock_lengths[best_stock_index]))
            index += accum_count[best_stock_index]
            total_wastage += best_wastage
            total_cost += self.stock_costs[best_stock_index]

            if index >= len(solution): done = True

        return points, total_wastage, total_cost


# csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])
csp = CSP(4, [5, 4, 6, 3], [1, 2, 3, 2], 1, [12], [10])
print(csp.decode([5, 4, 6, 3, 3, 4, 6, 6]))
