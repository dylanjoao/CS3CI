import random
import numpy as np
import time
from csp import CSP

POPULATION_N = 20


def evolution_search(csp, population_n, FITNESS_FUNC, limit):
    # init population
    population = [ csp.random_solution() for i in range(population_n) ]

    # select parents
    parents = proportionate_selection(population, FITNESS_FUNC)

    # produce offspring (recombination + mutation)
    

    # select survivors for next population
    print(f"E")

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
        



# # csp = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])

evolution_search_solution = evolution_search(csp, POPULATION_N, csp.evaluate_cost, 5.0)

# random_search_solution = random_search(csp, csp.random_solution, csp.evaluate_cost, 1.0)
# solution = random_search_solution
# patterns = csp.view_solution(solution)
# produced = csp.get_quantities_produced(solution)
# cost = csp.evaluate_cost(solution)
# wastage = csp.evaluate_wastage(solution)
# valid = csp.is_valid(solution)
# print(f"Solution {solution}\nPatterns: {patterns}\nProduced: {produced}\nCost: {cost}\nWastage: {wastage}\nValid: {valid}")