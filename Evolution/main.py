from tsp import TSP
import numpy as np
import copy
import time
import threading
import random
import math

################################################
# The novel variant is Inver-over operator for the TSP (Tao, G. and Michalewicz, Z., 1998)
################################################

# Tournament selection of 3
def select_parents(population, tsp, offsprings):
    parents = []

    for i in range(0, offsprings):
        best = []
        cost = 0
        subset = random.sample(population, 3)

        for j in range(0, len(subset)):
            _cost = tsp.evaluate_route(subset[j])
            if _cost < cost or cost == 0:
                cost = _cost
                best = subset[j]

        parents.append(best)

    return parents

# City swap mutation
def city_swap_mutate(route):
    neighbour = copy.deepcopy(route)
    r1 = random.randint(0, len(neighbour)-1)
    r2 = random.randint(0, len(neighbour)-1)
    neighbour[r1], neighbour[r2] = neighbour[r2], neighbour[r1]
    return neighbour

# Evolution search
def evolution_search(tsp, limit, n_population):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_route = []
    track = []

    population = [tsp.random_route() for i in range(n_population)]

    # while count < limit:
    while time.time() < end:

        parents = select_parents(population, tsp, n_population)
        _cost = 0

        # Recombine parents to form offsprings 100% of the time
        candidates = recombine_crossover(parents, n_population)

        # Mutate 70% of the time
        for i in range(len(candidates)):
            if random.randint(0, 100) > 69:
                candidates[i] = city_swap_mutate(candidates[i])

        # Evaluate new candidates
        for i in range(len(candidates)):
            _cost = tsp.evaluate_route(candidates[i])
            if _cost < best_cost:
                best_cost = _cost
                best_route = candidates[i]

        # Select new population
        population = candidates

        track.append(_cost)
        count += 1


    print(track)
    print(f"Best route after {count} iterations {best_route}, with cost {best_cost} [Evolution]")
    return best_route

# Produces 1 offspring from 2 parents
def recombine_crossover(parents, n_offsprings):
    route_length = len(parents[0])
    offsprings = []

    for i in range(n_offsprings):
        _parents = random.sample(parents, 2)

        offspring1 = [0 for i in range(route_length)]
        # offspring2 = [0 for i in range(route_length)]

        cutting_point = random.randint(0, route_length)

        amount = math.floor(float(route_length)/2)
        subset1 = circular_subset(_parents[0], cutting_point, amount)
        # subset2 = circular_subset(_parents[1], cutting_point, amount)

        for i in range(len(subset1)):
            offspring1[(i+cutting_point) % route_length] = subset1[i]
            # offspring2[(i+cutting_point) % route_length] = subset2[i]

        remaining1 = []
        # remaining2 = []
        index = cutting_point+amount
        while(len(remaining1) != route_length-amount):
            if (_parents[1][index % route_length] not in subset1):
                remaining1.append(_parents[1][index % route_length])
            index += 1

        # index = cutting_point+amount
        # while(len(remaining2) != route_length-amount):
        #     if (_parents[0][index % route_length] not in subset2):
        #         remaining2.append(_parents[0][index % route_length])
        #     index += 1

        index = cutting_point+amount
        for i in range(route_length-amount):
            offspring1[(index) % route_length] = remaining1[i]
            # offspring2[(index) % route_length] = remaining2[i]
            index += 1

        offsprings.append(offspring1)
        # offsprings.append(offspring2)

        # print(f"Parent 1: {_parents[0]}")
        # print(f"Parent 2: {_parents[1]}")
        # print(f"Subset 1: {subset1}")
        # print(f"Subset 2: {subset2}")
        # print(f"Offspring 1: {offspring1}")
        # print(f"Offspring 2: {offspring2}")

    return offsprings

def circular_subset(lst, start, length):
    subset = []
    for i in range(start, length+start):
        subset.append(lst[i % len(lst)])
    return subset


def evolution_inverover(tsp, limit, n_population):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_route = []
    track = []

    population = [tsp.random_route() for i in range(n_population)]

    while count < limit:
    # while time.time() < end:

        for i in range(len(population)):
            s1 = copy.deepcopy(population[i])
            s2 = copy.deepcopy(population[i])
            city_start_index = random.choice(s1)
            city_end_index = -1
            terminate = False

            while not terminate:

                if random.randint(0, 100) < 69:
                    city_end_index = random.choice([i for i in s1 if i != city_end_index])-1
                else:
                    s2 = random.choice(population)
                    city_end_index = s2.index(s1.index(city_start_index)+1)

                # In the next iteration if c' is next to c
                if (s1[city_start_index+1 % len(s1)] == s2[city_end_index]):
                    terminate = True

                s1 = invert_section_circular(s1, city_start_index, city_end_index)
                city_start_index = city_end_index

                _cost = tsp.evaluate_route(s1)
                if _cost <= tsp.evaluate_route(population[i]):
                    population[i] = s1
                    track.append(_cost)
        count += 1

    print("done")

def invert_section_circular(lst, start, end):
    length = len(lst)
    section_length = (end - start + 1) % length  # Calculate section length

    inverted_section = []
    for i in range(section_length):
        index = (start + i) % length
        inverted_section.append(lst[index])

    inverted_section = inverted_section[::-1]

    result = lst.copy()
    for i in range(section_length):
        index = (start + i) % length
        result[index] = inverted_section[i]

    return result

tsp = TSP([])
tsp.matrix_from_csv('ulysses16.csv')
# evolution_search(tsp, 3.0, 50)
evolution_inverover(tsp, 1, 10)

# s1 = [2, 3, 9, 4, 1, 5, 8, 6, 7]
# s2 = [1, 6, 4, 3, 5, 7, 9, 2, 8]
# city_start_index = 1
# city_start_address = s1[city_start_index]
# city_end_index = s2.index(s1.index(city_start_index)+1)
# city_end_address = s2[city_end_index]

# s3 = invert_section_circular(s1, city_start_index+1, city_end_index+1)

# # city_end_address = s2[city_end_index+1]
# print(f"Start Index: {city_start_index}, Address: {city_start_address}")
# print(f"End Index: {city_end_index}, Address: {city_end_address}")
# print(f"Final list {s3}")

