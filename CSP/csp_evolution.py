from copy import deepcopy
import math
import random
import numpy as np
import time
from csp import CSP


def evolution_search(csp, population_n, FITNESS_FUNC, limit):
    end = time.time() + limit # time + seconds
    best = None
    best_fitness = float('inf')
    prev_best = best_fitness
    minima = 0
    # init population
    population = [ csp.random_solution() for i in range(population_n) ]
    invalid_c = [ 0 for i in range(population_n)]

    # select parents
    parents = proportionate_selection(population, FITNESS_FUNC)

    count = 0
    # while count < limit:
    while time.time() < end:
        # produce offspring (recombination + mutation)
        offsprings = []
        
        while len(offsprings) is not population_n:
            s1 = random.choice(parents)
            s2 = random.choice(parents)
            child = recombine_half(s1, s2)

            # Mutation
            if random.uniform(0.0, 1.0) > 0.5:
                rs = csp.random_solution()
                ri = random.randint(0, csp.available_sizes-1)
                child[ri] = rs[ri]

            offsprings.append(child)

        # evaluate, if invalid replace solution
        for i in range(len(offsprings)):
            if not csp.is_valid(offsprings[i]): 
                offsprings[i] = csp.random_solution()
                continue
            fitness = FITNESS_FUNC(offsprings[i]) 
            if (fitness < best_fitness):
                best = offsprings[i]
                best_fitness = fitness

        # select survivors for next population
        # if minima has been reached reset population
        if (minima > 50):
            parents = [ csp.random_solution() for i in range(len(parents)) ]
            minima = 0
        else:
            parents = best_selection( offsprings, FITNESS_FUNC)
        

        # Calculate population invalidty
        invalid = 0
        for i in range(len(parents)):
            if not csp.is_valid(parents[i]): invalid += 1

        if (best_fitness < prev_best):
            prev_best = best_fitness
            print(f"Gen {count} best fitness {best_fitness}, {best}, invalid% {invalid/len(parents)*100}")
        else:
            minima += 1

        count += 1

    return best



# Returns a selection of 1/2 the population
def proportionate_selection(population, FITNESS_FUNC):
    selection = []
    weights = []
    total_fitness = 0

    for i in range(len(population)):
        total_fitness += FITNESS_FUNC(population[i])
    
    for i in range(len(population)):
        weights.append(FITNESS_FUNC(population[i])/total_fitness)

    for i in range(int(len(population)/2)):
        s = np.random.choice(len(population), p=weights)
        selection.append(population[s])

    return selection

# Returns a selection of 1/2 the population        
def best_selection(population, FITNESS_FUNC):
    sorted_p = deepcopy(population)
    sorted_p.sort(key=FITNESS_FUNC)
    return sorted_p[0:math.floor(len(population)/2)]



def recombine_stock_swap(ind1, ind2):
    child = []

    # For each stock
    for i in range(len(ind1)):
        if i % 2:
            child.append(ind1[i])
        else:
            child.append(ind2[i])

    return child

def recombine_half(ind1, ind2):
    child = []

    # For each stock
    for i in range(len(ind1)):

        # take the first half from both
        half1 = ind1[i][0:math.floor(len(ind1[i])/2)]
        half2 = ind2[i][0:math.floor(len(ind2[i])/2)]
        combination = half1 + half2

        child.append(combination)

    return child


csp = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
# csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])

solution = evolution_search(csp, 40, csp.evaluate_cost, 300.0)


# random_search_solution = random_search(csp, csp.random_solution, csp.evaluate_cost, 1.0)
patterns = csp.view_solution(solution)
produced = csp.get_quantities_produced(solution)
cost = csp.evaluate_cost(solution)
wastage = csp.evaluate_wastage(solution)
valid = csp.is_valid(solution)
print(f"Solution {solution}\nPatterns: {patterns}\nProduced: {produced}\nCost: {cost}\nWastage: {wastage}\nValid: {valid}")