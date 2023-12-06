
from copy import copy
from random import shuffle, randint, choices
from math import sqrt
from time import time


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
    
def random_search(csp, SOLUTION_FUNC, FITNESS_FUNC, limit):
    end = time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_solution = []

    # while count < limit:
    while time() < end:
        solution = SOLUTION_FUNC()
        fitness = FITNESS_FUNC(solution)

        if (fitness < best_cost):
            best_cost = fitness
            best_solution = solution

        count += 1

    print(f"Best solution after {count} iterations with fitness {best_cost} [Random Search]")
    return best_solution

def evolution_search(csp, population_n, SOLUTION_FUNC, FITNESS_FUNC, limit):
    generation = 0
    population = [ SOLUTION_FUNC() for _ in range(population_n) ]
    population_cost = []
    
    for i in range(len(population)):
        population_cost.append(FITNESS_FUNC(population[i]))

    offsprings = []
    for i in range(len(population)):
        offsprings.append(mutate_3ps(population[i]))


def mutate_3ps(individual):
    # item 1 select randomly from ordererd list
    # item 2 and 3
    # - select stock cut with weighted probabilty
    # - select random item within stock cut
    
    decoded = csp.decode(individual)
    offspring = copy(individual)
    solution_length = len(decoded["solution"])
    weights = [ 0 for _ in range(solution_length)]
    
    w_all = 0

    for i in range(solution_length):
        if not decoded["solution"][i]["waste"] == 0:
            w_all += sqrt(1/decoded["solution"][i]["waste"])

    for j in range(solution_length):
        w = decoded["solution"][j]["waste"]            # Wastage of the jth stock
        if w == 0: continue
        weights[j] = sqrt(1/w)/w_all

    indexes = [randint(0, len(individual))]
    
    done = False

    while not done:

        stock_index = choices(range(solution_length), weights=weights)[0]
        stock = decoded["solution"][stock_index]
        stock_next = decoded["solution"][(stock_index%(solution_length-1))+1]
        points = [stock["point"], stock_next["point"]]
        points = sorted(points)
        index = randint(points[0], points[1]-1)

        if index not in indexes:
            indexes.append(index)
        if len(indexes) == 3:
            done = True

    for i in range(1, len(indexes)):
        offspring[indexes[i - 1]], offspring[indexes[i]] = offspring[indexes[i]], offspring[indexes[i - 1]]

    return offspring





# csp = CSP(18, 
#           [2350, 2250, 2200, 2100, 2050, 2000, 1950, 1900, 1850, 1700, 1650, 1350, 1300, 1250, 1200, 1150, 1100, 1050], 
#           [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3],
#           8,
#           [4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500],
#           [86, 85, 83, 79, 68, 66, 64, 63]
#           )
# csp = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
# csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])
csp = CSP(4, [5, 4, 6, 3], [1, 2, 3, 2], 1, [12], [10])

# random_search(csp, csp.random_solution, csp.evaluate, 5.0)
evolution_search(csp, 10, csp.random_solution, csp.evaluate, 5.0)
