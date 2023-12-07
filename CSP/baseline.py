from csp_order import CSP
from copy import copy
from random import shuffle, randint, choices
from math import sqrt
from time import time
from threading import Thread

class Individual:
    def __init__(self, fitness_func, solution):
        self.solution = solution
        self.fitness = fitness_func(solution)
        self.wins = 0

def random_search(out, csp, SOLUTION_FUNC, FITNESS_FUNC, limit, verbose=0):
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

    decoded = csp.decode(best_solution)
    info = ""
    info += (f"[Random Search] Best solution after {count} iterations, with fitness {best_cost}, waste {decoded["total_wastage"]}, cost {decoded["total_cost"]}")
    if verbose: info += (f"\n{csp.get_solution_info(best_solution)}")
    print(info)
    
    out.extend(best_solution)

    return best_solution

def evolution_search(out, csp, population_n, SOLUTION_FUNC, FITNESS_FUNC, limit, verbose=0):
    end = time() + limit
    generation = 1
    population = []
    
    for i in range(population_n):
        s = SOLUTION_FUNC()
        population.append(Individual(FITNESS_FUNC, s))

    best_solution = None
    best_fitness = float('inf')

    # Double mutation
    # while generation < limit:
    while time() < end:
        offsprings = []

        # Produce offspring
        for i in range(population_n):
            s = mutate_3ps(mutate_3ps(population[i].solution))
            offsprings.append(Individual(FITNESS_FUNC, s))

        all_individuals = population + offsprings
        
        # Select parents
        for i in range(len(all_individuals)):
            for q in range(10):  # Perform 10 pairwise comparisons for each individual
                opponent_index = randint(0, len(all_individuals)-1)
                if all_individuals[i].fitness <= all_individuals[opponent_index].fitness:
                    all_individuals[i].wins += 1

        
        winners = sorted(all_individuals, key=lambda Individual: Individual.wins, reverse=True)[:population_n]
        population = winners

        for i in range(len(winners)):
            winners[i].wins = 0
            if winners[i].fitness < best_fitness:
                best_solution = winners[i].solution
                best_fitness = winners[i].fitness
                if verbose > 0: print(f"Generation {generation} with fitness {best_fitness}")

        generation += 1

    decoded = csp.decode(best_solution)
    info = ""
    info += (f"[EA Search] Best solution after {generation} generations, with fitness {best_fitness}, waste {decoded["total_wastage"]}, cost {decoded["total_cost"]}")
    if verbose > 1: info += (f"\n{csp.get_solution_info(best_solution)}")
    print(info)

    if type(out) == list: out.extend(best_solution)

    return best_solution

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

    wastage_percent = 0

    for i in range(solution_length):
        if not decoded["solution"][i]["waste"] == 0:
            w_all += sqrt(1/decoded["solution"][i]["waste"])

    for j in range(solution_length):
        w = decoded["solution"][j]["waste"]            # Wastage of the jth stock
        if w == 0: continue
        weights[j] = sqrt(1/w)/w_all

    indexes = [randint(0, len(individual)-1)]
    
    done = False

    for _ in range(2):

        if sum(weights) == 0.0:
            stock_index = randint(0, solution_length-1)
        else:
            stock_index = choices(range(solution_length), weights=weights)[0]

        stock = decoded["solution"][stock_index]
        stock_next = decoded["solution"][(stock_index%(solution_length-1))+1]
        points = [stock["point"], stock_next["point"]]
        points = sorted(points)
        index = randint(points[0], points[1]-1)

        # if index not in indexes:
        indexes.append(index)
        # if len(indexes) == 3:
        #     break

    for i in range(1, len(indexes)):
        offspring[indexes[i - 1]], offspring[indexes[i]] = offspring[indexes[i]], offspring[indexes[i - 1]]

    return offspring


csp = CSP(18, 
          [2350, 2250, 2200, 2100, 2050, 2000, 1950, 1900, 1850, 1700, 1650, 1350, 1300, 1250, 1200, 1150, 1100, 1050], 
          [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3],
          8,
          [4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500],
          [86, 85, 83, 79, 68, 66, 64, 63]
          )
# csp = CSP(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
# csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 190])
# csp = CSP(4, [5, 4, 6, 3], [1, 2, 3, 2], 1, [12], [10])


random_solution = []
ea_solution = []

threads = []

duration = 5 * 60

t1 = Thread(target=random_search, args=(random_solution, csp, csp.random_solution, csp.evaluate_waste, duration, 0))
t2 = Thread(target=evolution_search, args=(ea_solution, csp, 15, csp.random_solution, csp.evaluate_waste, duration, 0))
t4 = Thread(target=evolution_search, args=(ea_solution, csp, 15, csp.random_solution, csp.evaluate_cost, duration, 1))
t6 = Thread(target=evolution_search, args=(ea_solution, csp, 15, csp.random_solution, csp.evaluate, duration, 0))

t1.start()
t2.start()
t4.start()
t6.start()

t1.join()
t2.join()
t4.join()
t6.join()
