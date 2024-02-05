import itertools
from csp_order import CSP_Novel
from copy import copy
from random import shuffle, randint, choices, sample
from math import ceil, sqrt
from time import time
import argparse

def novel_search(out, csp, population_n, max_age, SOLUTION_FUNC, FITNESS_FUNC, limit, verbose=0):
    ## DATA
    data = { "best_fitness": float('inf'), "gen_found_at": -1, "time_found_at": -1, "waste": [], "cost": [] }
    generational_best = []  # [ (fitness, time), (fitness, time) ]
    ##
    
    start = time()
    end = time() + limit
    generation = 0
    population = [[SOLUTION_FUNC(), 0] for _ in range(population_n)]

    best_solution = None
    best_fitness = float('inf')

    # while generation < limit:
    while time() < end:
        ## DATA
        _gen_best_sol = []
        _gen_best = [ float('inf'), -1.0 ] 
        ##

        offsprings = []

        # Produce offspring
        for i in range(population_n):
            s = genetic_offspring(population[i][0], csp)
            offsprings.append([s, population[i][1]])

        # Select parents based on fitness
        parents = []
        for i in range(len(offsprings)):
            fitness = FITNESS_FUNC(offsprings[i][0])
            offsprings[i][1] += 1
            parents.append((offsprings[i], fitness))
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = offsprings[i][0]
                if verbose > 0: print(f"Gen {generation} with fitness {best_fitness:.9f} after {(time()-start):.2f}s")

                ## DATA
                data["best_fitness"] = fitness
                data["gen_found_at"] = generation
                data["time_found_at"] = time()-start
                ##

            ## DATA
            if fitness < _gen_best[0]:
                _gen_best[0] = fitness
                _gen_best[1] = time()-start
                _gen_best_sol = offsprings[i][0]
            ##


        parents.sort(key=lambda x: x[1], reverse=False)
        population = [ x[0] for x in parents[:population_n] ]

        for i in range(len(population)):
            if population[i][1] > max_age:
                population[i] = [SOLUTION_FUNC(), 0]

        generation += 1
        ## DATA
        generational_best.append(_gen_best)
        _gd = csp.decode(_gen_best_sol)
        data["waste"].append(_gd["total_wastage"])
        data["cost"].append(_gd["total_cost"])
        #

    decoded = csp.decode(best_solution)
    info = ""
    info += (f"[Novel Search] Best in {generation} generations, with fitness {csp.evaluate(best_solution)}, waste {decoded["total_wastage"]}, cost {decoded["total_cost"]} after {(time()-start):.2f}s")
    if verbose > 1: info += (f"\n{csp.get_solution_info(best_solution)}")
    print(info)

    if type(out) == list: out.append((data, generational_best))

    return best_solution

def genetic_offspring(solution, csp):
    chromosone = solution

    start_summation = sum(solution)

    genes_fit = []
    genes_leftover = []
    chromosone_child = []
    chromosone_leftover = []

    # Check and obtain fit genes
    genes_fit, genes_leftover, chromosone_child, chromosone_leftover = obtain_genes(chromosone, csp)
    
    if len(genes_fit) == 0: return mutate_3ps(solution)

    # Try to combine to form fit genes
    combined, chromosone_leftover = combine_for_fit(genes_leftover, genes_fit)
    chromosone_child += combined

    # Local chromosone mutation loop
    best_mutation = None
    best_mutation_wastage = float('inf')
    k = 0
    
    while k < 30:
        # Mutate leftover
        mutated = mutate_3ps(chromosone_leftover)
        d = csp.decode(mutated)

        # Find fit genes and append to child
        _fit_genes, _unfit_genes, _c_child, _c_leftover = obtain_genes(mutated, csp)
        chromosone_child += _c_child
        chromosone_leftover = _c_leftover

        # Try to combine to form fit genes
        if (len(_fit_genes) > 0):
            _combined, _c_leftover = combine_for_fit(_unfit_genes, _fit_genes+genes_fit)
            chromosone_child += _combined
            chromosone_leftover = _c_leftover
    
        if d["total_wastage"] < best_mutation_wastage:
            best_mutation = mutated
            best_mutation_wastage = d["total_wastage"]
            k = 0
        else:
            k += 1

    full_chromosone = chromosone_child + chromosone_leftover
    summation = sum(full_chromosone)

    return full_chromosone

def obtain_genes(chromosone, csp):
    decoded = csp.decode(chromosone)

    genes_fit = []
    genes_leftover = []
    chromosone_child = []
    chromosone_leftover = []

    # Check and obtain fit genes
    for i in range(len(decoded["solution"])):
        gene = chromosone[0 if i == 0 else decoded["solution"][i-1]["point"]:decoded["solution"][i]["point"]]
        if decoded["solution"][i]["waste"] > 0:
            genes_leftover.append(gene)
            chromosone_leftover += gene
            continue

        chromosone_child += gene
        exists = False
        for _fit_gene in genes_fit:
            if sorted(gene) == sorted(_fit_gene): exists = True
        if not exists:
            genes_fit.append(gene)
        
    return genes_fit, genes_leftover, chromosone_child, chromosone_leftover

def combine_for_fit(genes_leftover, genes_fit):
    chromosone = []
    genes_leftover_copy = genes_leftover.copy()
    chromosone_leftover = []
    to_be_popped = []

    for geneA, geneB in itertools.combinations( enumerate(genes_leftover), 2 ):
        for _fit_gene in genes_fit:
            _new_gene = geneA[1] + geneB[1]
            if sorted(_new_gene) == sorted(_fit_gene):
                # Append to chromosone_child and pop from chromosone_leftover
                chromosone += _new_gene
                to_be_popped.append(geneA[0])
                to_be_popped.append(geneB[0])

    for i in range(len(to_be_popped)):
        genes_leftover_copy.pop(to_be_popped[i]-i)
    
    for i in range(len(genes_leftover_copy)):
        chromosone_leftover += genes_leftover_copy[i]

    return chromosone, chromosone_leftover

def mutate_3ps(individual):
    if len(individual) < 3: return individual
    offspring = individual.copy()
    indexes = sample(range(len(offspring)), 3)
    offspring[indexes[0]], offspring[indexes[1]], offspring[indexes[2]] = \
        offspring[indexes[2]], offspring[indexes[0]], offspring[indexes[1]]

    return offspring

csp = CSP_Novel(36, 
          [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67],
          [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17],
          5,
          [120, 115, 110, 105, 100],
          [12, 11.5, 11, 10.5, 10]
          )
# csp = CSP_Novel(18, 
#           [2350, 2250, 2200, 2100, 2050, 2000, 1950, 1900, 1850, 1700, 1650, 1350, 1300, 1250, 1200, 1150, 1100, 1050], 
#           [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3],
#           8,
#           [4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500],
#           [86, 85, 83, 79, 68, 66, 64, 63]
#           )
# csp = CSP_Novel(8, [3, 4, 5, 6, 7, 8, 9, 10], [5, 2, 1, 2, 4, 2, 1, 3], 3, [10, 13, 15], [100, 130, 150])
# csp = CSP_Novel(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 190])
# csp = CSP_Novel(4, [3, 4, 5, 6], [4, 2, 2, 4], 1, [12], [100])

if __name__ == '__main__':
    novel_solution = []

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-e", "--evaluation", help="e.g. fitness, cost, waste, costwaste", required=True)
    argParser.add_argument("-p", "--population", help="Number of inital population", type=int, default=5)
    argParser.add_argument("-a", "--age", help="Maximum age of each individual", type=int, default=2)
    argParser.add_argument("-t", "--time", help="Duration to run the algorithm", type=float, default=5.0)
    argParser.add_argument("-v", "--verbose", help="Print information", type=int, default=1)

    args = argParser.parse_args()
    evaluation = None

    match args.evaluation:
        case "fitness": evaluation = csp.evaluate
        case "cost": evaluation = csp.evaluate_cost
        case "waste": evaluation = csp.evaluate_waste
        case "costwaste": evaluation = csp.evaluate_cost_waste

    novel_search(novel_solution, csp, args.population, args.age, csp.random_solution, evaluation, args.time, args.verbose)

# novel_search(novel_solution, csp, 5, 3, csp.random_solution, csp.evaluate, 300.0, 1)

# python novel.py -e fitness -p 3 -a 3 -t 100.0 -v 1



