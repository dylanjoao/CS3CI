import itertools
from csp_order import CSP_Novel
from copy import copy
from random import shuffle, randint, choices
from math import ceil, sqrt
from time import time
import argparse

def novel_search(out, csp, population_n, SOLUTION_FUNC, FITNESS_FUNC, limit, verbose=0):
    end = time() + limit
    generation = 0

    best_solution = None
    best_fitness = float('inf')

    while generation < limit:
    # while time() < end:
        
        chromosone = None
        has_fit_genes = False

        genes_fit = []
        genes_unfit = []
        chromosone_leftover = []
        chromosone_child = []

        # Obtain fit genes
        while not has_fit_genes:
            chromosone = [6, 3, 3, 5, 4, 4, 6, 6, 3, 5, 6, 3]
            d = csp.decode(chromosone)
            for i in range(len(d["solution"])):
                gene = chromosone[0 if i == 0 else d["solution"][i-1]["point"]:d["solution"][i]["point"]]
                if d["solution"][i]["waste"] > 0: 
                    genes_unfit.append(gene)
                    continue
                has_fit_genes = True
                chromosone_child += gene
                if gene not in genes_fit: genes_fit.append(gene)
        
        # Find any combinations to form fit genes
        for geneA, geneB in itertools.combinations( enumerate(genes_unfit), 2 ):
            for fit_gene in genes_fit:
                new_gene = geneA[1] + geneB[1]
                if sorted(new_gene) == sorted(fit_gene):
                    # Append to chromosone_child and pop from chromosone_leftover
                    chromosone_child += new_gene
                    genes_unfit.pop(geneA[0])
                    genes_unfit.pop(geneB[0]-1)
                    
        for unfit_gene in genes_unfit:
            chromosone_leftover += unfit_gene

        # Evolve left over chromosone to obtain fit genes

        best_mutation = None
        best_mutation_waste = float('inf')
        
        k = 0
        while k < 30:
            mutated = mutate_3ps(chromosone_leftover)
            d = csp.decode(mutated)
            waste = d["total_wastage"]

            # Check for fit genes in the leftover space
            for i in range(len(d["solution"])):
                gene = chromosone[0 if i == 0 else d["solution"][i-1]["point"]:d["solution"][i]["point"]]
                if d["solution"][i]["waste"] > 0: continue  # If gene waste is not 0 skip
                if gene in genes_fit: continue     # If gene already in leftover skip
                genes_fit.append(gene)
            
            if waste < best_mutation_waste:
                best_mutation = mutated
                best_mutation_waste = waste
                k = 0
            else:
                k += 1



        # combine any genes capable of making a fit gene from the above list

        # keep genes that produce 0 waste
        # combine any genes capable of making a fit gene from the above list
        # create a child chromosone with only fit genes

        # evolve (mutate?) the leftover chromosone (meaning exclude the fit genes only the unfit genes)
        #   if the number of evolutions that results in more or same total wastage


        generation += 1

    # decoded = csp.decode(best_solution)
    # info = ""
    # info += (f"[Novel Search] Best solution after {generation} generations, with fitness {best_fitness}, waste {decoded["total_wastage"]}, cost {decoded["total_cost"]}")
    # if verbose > 1: info += (f"\n{csp.get_solution_info(best_solution)}")
    # print(info)

    # if type(out) == list: out.extend(best_solution)

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
csp = CSP_Novel(4, [5, 4, 6, 3], [1, 2, 3, 2], 1, [12], [10])

# c = Chromosone(csp.evaluate, csp.decode, [30, 20, 25, 30, 25, 20, 25, 25, 20, 30, 30, 25, 20, 30, 20, 25, 25] )
# print(csp.get_solution_info([30, 20, 25, 25, 30, 20, 25, 25, 20, 30, 30, 25, 20, 30, 20, 25, 25]))

novel_solution = []

novel_search(novel_solution, csp, 20, csp.random_solution, csp.evaluate, 1.0, 1)

l = [5, 6, 9, 12, 1, 0]
l.pop(2)
l.pop(4-1)
print(l)

# argParser = argparse.ArgumentParser()
# argParser.add_argument("-e", "--evaluation", help="e.g. fitness, cost, waste, costwaste", required=True)
# argParser.add_argument("-p", "--population", help="Number of inital population", type=int, default=20)
# argParser.add_argument("-t", "--time", help="Duration to run the algorithm", type=float, default=5.0)
# argParser.add_argument("-v", "--verbose", help="Print information", type=int, default=1)

# args = argParser.parse_args()
# evaluation = None

# match args.evaluation:
#     case "fitness": evaluation = csp.evaluate
#     case "cost": evaluation = csp.evaluate_cost
#     case "waste": evaluation = csp.evaluate_waste
#     case "costwaste": evaluation = csp.evaluate_cost_waste

# evolution_search(ea_solution, csp, args.population, csp.random_solution, evaluation, args.time, args.verbose)

# python baseline.py -e fitness -p 20 -t 60.0 -v