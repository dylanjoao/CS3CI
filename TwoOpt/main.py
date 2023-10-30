from tsp import TSP
import numpy as np
import copy
import time
import threading

# Generate a neighbourhood from a route
def city_swap_neighbourhood(route):
  neighbours = []
  for i in range(1,len(route)):
    for j in range(i+1,len(route)):
      neighbour = copy.deepcopy(route)
      neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
      neighbours.append(neighbour)
  return neighbours

# Find the best solution in a neighbourhood
def neighbourhood_step(tsp, neighbourhood):
    best_cost = float('inf')
    best_index = -1

    for index, route in enumerate(neighbourhood):
        cost = tsp.evaluate_route(route)
        if (cost < best_cost):
            best_cost = cost
            best_index = index

    return neighbourhood[best_index]

# Local search using city swaps
def local_search(tsp, limit):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_route = []

    # while count < limit:
    while time.time() < end:

        tour = tsp.random_route()
        neighbouring_routes = city_swap_neighbourhood(tour)
        best_neighbour = neighbourhood_step(tsp, neighbouring_routes)

        cost = tsp.evaluate_route(best_neighbour)
        if (cost < best_cost):
            best_cost = cost
            best_route = best_neighbour

        count += 1

    print(f"Best route after {count} iterations {best_route}, with cost {best_cost} [Local Search]")
    return best_route

# Random search
def random_search(tsp, limit):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_route = []

    # while count < limit:
    while time.time() < end:
        route = tsp.random_route()
        cost = tsp.evaluate_route(route)

        if (cost < best_cost):
            best_cost = cost
            best_route = route

        count += 1

    print(f"Best route after {count} iterations {best_route}, with cost {best_cost} [Random Search]")
    return best_route

tsp = TSP([])
tsp.matrix_from_csv('ulysses16.csv')

t1 = threading.Thread(target=local_search, args=(tsp, 3.0))
t2 = threading.Thread(target=random_search, args=(tsp, 3.0))

t1.start()
t2.start()

t1.join()
t2.join()