
from random import shuffle
from math import sqrt

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
        self.requested_quantity = q     # { 5,  7,  5 }

        self.stock_n = m                # 3
        self.stock_lengths = l          # { 50, 80, 100 }
        self.stock_costs = c            # { 100, 175, 250 }

    def random_solution(self):
        items = [length for length, quantity in zip(self.requested_length, self.requested_quantity) for _ in range(quantity)]
        shuffle(items)
        return items

    # 5  4  6  3  3  4  6  6  
    # return cutting points, wastage, cost
    # greedy search 
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
            
            points.append({"point": index+accum_count[best_stock_index], "stock": self.stock_lengths[best_stock_index], "waste": best_wastage})
            index += accum_count[best_stock_index]
            total_wastage += best_wastage
            total_cost += self.stock_costs[best_stock_index]

            if index >= len(solution): done = True

        return {"solution": points, "total_wastage": total_wastage, "total_cost": total_cost}
    
    # K.-H. Liang et al. / Computers & Operations Research 29 (2002) 1641-1659
    # Eq 9
    def evaluate(self, solution):
        decoded = self.decode(solution)
        m = len(decoded["solution"])

        term1 = 0
        term2 = 0
        for j in range(m):
            # term 1
            w = decoded["solution"][j]["waste"]            # Wastage of the jth stock
            l = decoded["solution"][j]["stock"]            # stock length of jth stock
            term1 += sqrt((w/l))

            # term 2
            v = 1 if (decoded["solution"][j]["waste"] > 0) else 0
            term2 += v/m
                
        fitness = (1/(m+1))*(term1+term2)

        return fitness

    def evaluate_cost(self, solution):
        return self.decode(solution)["total_cost"]

    def get_solution_info(self, solution):
        decoded = self.decode(solution)
        cutting_points = [info["point"] for info in decoded["solution"]]
        costs = [self.stock_costs[self.stock_lengths.index(info["stock"])] for info in decoded["solution"]]
        lengths = [info["stock"] for info in decoded["solution"]]
        wastages = [info["waste"] for info in decoded["solution"]]

        info = ""
        info += ("Solution:    {}\n".format(solution))
        info += ("Cost:        | {} |\n".format(" | ".join("{:3}".format(cost) for cost in costs)))
        info += ("Length:      | {} |\n".format(" | ".join("{:3}".format(length) for length in lengths)))
        info += ("Wastage:     | {} |".format(" | ".join("{:3}".format(wastage) for wastage in wastages)))

        return info


