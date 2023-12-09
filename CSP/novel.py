import itertools
from csp_order import CSP_Novel
from copy import copy
from random import shuffle, randint, choices
from math import ceil, sqrt
from time import time
import argparse

# Chromosone contains genes
class Chromosone:
    def __init__(self):
        self.genes = []

    def to_chromosone(self, decode_func, solution):
        decoded = decode_func(solution)
        decoded_solution = decoded["solution"]

        gene = solution[0:decoded_solution[0]["point"]]
        self.genes.append(Gene(gene))

        for i in range(len(decoded_solution)-1):
            current = decoded_solution[i]["point"]
            next = decoded_solution[i+1]["point"]
            self.genes.append(Gene(solution[current:next]))

    def get_solution(self):
        s = []
        for i in range(len(self.genes)):
            s += self.genes[i].gene
        return s

# Gene contains patterns of solution
class Gene:
    def __init__(self, pattern):
        self.gene = pattern


def novel_search(out, csp, population_n, SOLUTION_FUNC, FITNESS_FUNC, limit, verbose=0):
    end = time() + limit
    generation = 1

    best_solution = None
    best_fitness = float('inf')

    # while generation < limit:
    while time() < end:
        
        prev_gen_best_chromosone = None

        # while no fit genes
        #   generate chromosone
        # c = Chromosone(csp.decode, SOLUTION_FUNC())
        chromosone = Chromosone()
        chromosone.to_chromosone(csp.decode, [5, 4, 6, 3, 3, 4, 6, 6, 3, 5, 6, 3])
        chromosone_waste = csp.decode(chromosone.get_solution())["total_wastage"]

        fit_genes_index = [ 0 for i in range(len(chromosone.genes)) ]
        has_fit_genes = False

        fit_chromosone = []
        remaining_chromosone = []
        child_chromosone = []
        point = 0

        # keep genes that produce 0 waste
        while not has_fit_genes:
            for i in range(len(chromosone.genes)):
                decoded = csp.decode(chromosone.genes[i].gene)
                if decoded["total_wastage"] > 0: 
                    remaining_chromosone += chromosone.genes[i].gene
                    continue
                has_fit_genes = True
                fit_genes_index[i] = 1
                fit_chromosone += chromosone.genes[i].gene

        k = 0
        local_chromosone = None
        local_chromosone_waste = float('inf')
        while k < 30:
            mutated = mutate_3ps(remaining_chromosone)
            c = fit_chromosone+mutated
            d = csp.decode(c)
            if d["total_wastage"] < local_chromosone_waste:
                local_chromosone = c
                local_chromosone_waste = d["total_wastage"]
                k = 0

                

            else: k+=1

        # combine any genes capable of making a fit gene from the above list
        # for item1, item2 in itertools.combinations( enumerate(remaining), 2):
        #     combined = item1[1].gene + item2[1].gene
        #     for i in fit_genes:
        #         if not i: continue
        #         if combined == chromosone.genes[i].gene:
        #             print("true")
        #             child.append(Gene(combined))
                    
        


        # combine any genes capable of making a fit gene from the above list
        


        # keep genes that produce 0 waste
        # combine any genes capable of making a fit gene from the above list
        # create a child chromosone with only fit genes

        # evolve (mutate?) the leftover chromosone (meaning exclude the fit genes only the unfit genes)
        #   if the number of evolutions that results in more or same total wastage


        generation += 1

    decoded = csp.decode(best_solution)
    info = ""
    info += (f"[Novel Search] Best solution after {generation} generations, with fitness {best_fitness}, waste {decoded["total_wastage"]}, cost {decoded["total_cost"]}")
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

novel_search(novel_solution, csp, 20, csp.random_solution, csp.evaluate, 5.0, 1)

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