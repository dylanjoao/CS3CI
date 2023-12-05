from deap import creator, base, tools, algorithms
import numpy as np
from csp import CSP


csp = CSP(3, [20, 25, 30], [5, 7, 5], 3, [50, 80, 100], [100, 175, 250])

# Minimisation of cost and wastage
creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Need to model an "individual"

IND_SIZE=10

# An individual contains patterns
# perhaps, [2, 19, 12, 15, 63]
# 2 being the stock length followed by pattern indexes

toolbox.register("attr_patterns", csp.random_solution)

toolbox.register("individual", tools.initCycle, creator.Individual, toolbox.attr_patterns, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalSolution(individual):
    return csp.evaluate_cost(individual), csp.evaluate_wastage(individual)

toolbox.register("evaluate", evalSolution)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian)
toolbox.register("select", tools.selNSGA2)

def main():
    NGEN = 50
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    algorithms.eaSimple(population=pop, toolbox=toolbox, mutpb=MU, cxpb=CXPB, ngen=NGEN, stats=stats,
                              halloffame=hof)

    return pop, stats, hof

main()