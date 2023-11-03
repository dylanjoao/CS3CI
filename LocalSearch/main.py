from tsp import TSP
import numpy as np
import copy
import time
import threading

################################################
# The novel variant is two opt swap
################################################

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

    pb_cost = float('inf')

    tour = tsp.random_route()
    track = []

    # while count < limit:
    while time.time() < end:

        improved = False
        neighbouring_routes = city_swap_neighbourhood(tour)
        best_neighbour = neighbourhood_step(tsp, neighbouring_routes)

        cost = tsp.evaluate_route(best_neighbour)
        if (cost < best_cost):
            best_cost = cost
            best_route = best_neighbour

        tour = best_neighbour
        track.append(cost)
        count += 1

        if cost < pb_cost:
            improved = True
            pb_cost = cost

        if not improved:
            tour = tsp.random_route()
            pb_cost = float('inf')
            track.append('REACHED')

    # print(*track, sep='\n')
    print(f"Best route after {count} iterations {best_route}, with cost {best_cost} [City Swap]")
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

# Local Search using two opt
def twoopt_search(tsp, limit):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_route = []

    pb_cost = float('inf')

    tour = tsp.random_route()
    track = []

    # while count < limit:
    while time.time() < end:

        improved = False
        neighbouring_routes = twoopt_neighbourhood(tour)
        best_neighbour = neighbourhood_step(tsp, neighbouring_routes)

        cost = tsp.evaluate_route(best_neighbour)
        if (cost < best_cost):
            best_cost = cost
            best_route = best_neighbour

        tour = best_neighbour
        track.append(cost)
        count += 1

        if cost < pb_cost:
            improved = True
            pb_cost = cost
            print(f"Better tour: {tour}, Cost: {cost}")

        if not improved:
            tour = tsp.random_route()
            pb_cost = float('inf')
            print("Randomising...")
            # track.append('REACHED')


    # print(*track, sep='\n')
    print(f"Best route after {count} iterations {best_route}, with cost {best_cost} [Two Opt]")
    return best_route

# Generate neighbourhood using two opt
def twoopt_neighbourhood(route):
    neighbours = []
    for i in range(1,len(route)-1):
        for j in range(i+1,len(route)):
            neighbour = copy.deepcopy(route)
            neighbours.append(twopt_swap(neighbour, i, j))
    return neighbours

# Two opt swap
def twopt_swap(route, vertex1, vertex2):
    new_route = []
    new_route.extend(route[0:vertex1+1])
    new_route.extend(route[vertex1+1:vertex2+1][::-1])
    new_route.extend(route[vertex2+1:])

    return new_route


tsp = TSP([])
tsp.matrix_from_csv('ulysses16.csv')

t1 = threading.Thread(target=local_search, args=(tsp, 5.0))
t2 = threading.Thread(target=random_search, args=(tsp, 5.0))
t3 = threading.Thread(target=twoopt_search, args=(tsp, 5.0))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# print(TwoOptSwap([1,2,6,5,4,3,7,8], 1, 5))