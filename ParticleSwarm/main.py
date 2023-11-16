from antennaarray import AntennaArray
import time
import copy
import random
import math
import threading

################################################
# The novel variant is the CONSTRICTION FACTOR by Clerc and Kennedy
################################################

def random_search(antenna, limit):
    end = time.time() + limit # time + seconds

    count = 0
    best_cost = float('inf')
    best_route = []

    # while count < limit:
    while time.time() < end:
        route = antenna.random_design()
        cost = antenna.evaluate(route)

        if (cost < best_cost):
            best_cost = cost
            best_route = route

        count += 1

    print(f"Best design after {count} iterations {best_route}, with cost {best_cost} [Random Search]")
    return best_route

def pso_search(antenna, limit, n_population):
    end = time.time() + limit # time + seconds

    population = [Particle(antenna.random_design(), antenna) for i in range(n_population)]

    g_best_cost = float('inf')
    g_best_particle = None

    CO1 = 0.72134752044
    CO2 = 1.19314718056

    count = 0

    # while count < limit:
    while time.time() < end:

        for particle in population:
            _cost = antenna.evaluate(particle.position)
            if (_cost < g_best_cost):
                g_best_cost = _cost
                g_best_particle = copy.deepcopy(particle)

        for particle in population:
            r1 = random.uniform(0.0,1.0)
            r2 = random.uniform(0.0,1.0)

            # Update position then velocity
            for i in range(len(particle.position)-1):
                particle.position[i] += particle.velocity[i]
                particle.velocity[i] = CO1*particle.velocity[i]+CO2*r1 * (particle.pb_position[i]-particle.position[i])+CO2*r2 * (g_best_particle.position[i]-particle.position[i])

            # Evaluate new position and Update personal best
            if not antenna.is_valid(particle.position):
                continue

            _cost = antenna.evaluate(particle.position)
            if _cost < particle.pb_cost:
                particle.pb_position = copy.deepcopy(particle.position)
                particle.pb_cost = _cost

        count += 1

        # print(g_best_particle)

    print(f"Best design after {count} iterations {g_best_particle.position}, with cost {g_best_cost:.20f} [PSO Search]")
    return g_best_particle.position

def pso_constriction_search(antenna, limit, n_population):
    end = time.time() + limit # time + seconds

    population = [Particle(antenna.random_design(), antenna) for i in range(n_population)]

    g_best_cost = float('inf')
    g_best_particle = None

    CO1 = 0.72134752044 * 2.1
    CO2 = 1.19314718056 * 2.1

    phi = CO1 + CO2

    # Controls balance between exploration and exploitation
    K = 0.35

    CF = 2*K/(abs(2-phi-math.sqrt(phi**2 - 4*phi)))

    count = 0

    # while count < limit:
    while time.time() < end:

        for particle in population:
            _cost = antenna.evaluate(particle.position)
            if (_cost < g_best_cost):
                g_best_cost = _cost
                g_best_particle = copy.deepcopy(particle)

        for particle in population:
            r1 = random.uniform(0.0,1.0)
            r2 = random.uniform(0.0,1.0)

            # Update position then velocity
            for i in range(len(particle.position)-1):
                particle.position[i] += particle.velocity[i]
                particle.velocity[i] = CF*(CO1*particle.velocity[i]+CO2*r1 * (particle.pb_position[i]-particle.position[i])+CO2*r2 * (g_best_particle.position[i]-particle.position[i]))

            # Evaluate new position and Update personal best
            if not antenna.is_valid(particle.position):
                continue

            _cost = antenna.evaluate(particle.position)
            if _cost < particle.pb_cost:
                particle.pb_position = copy.deepcopy(particle.position)
                particle.pb_cost = _cost

        count += 1

        print(g_best_particle)

    print(f"Best design after {count} iterations {g_best_particle.position}, with cost {g_best_cost:.20f} [PSO Constriction Search]")
    return g_best_particle.position


class Particle:
    pb_position = []
    pb_cost = float('inf')
    position = []
    velocity = []

    def __init__(self, position, antenna):
        self.position = position
        self.pb_position = copy.deepcopy(position)
        self.pb_cost = antenna.evaluate(position)

        _v = antenna.random_design()

        for i in range(len(_v)-1):
            _v[i] = (_v[i]+self.position[i])/2

        self.velocity = _v


    def __str__(self):
        return f"Position: {self.pb_position}, Cost: {self.pb_cost:.20f}"


antenna = AntennaArray(4, 55)


t1 = threading.Thread(target=random_search, args=(antenna, 10.0))
t2 = threading.Thread(target=pso_search, args=(antenna, 10.0, 12))
t3 = threading.Thread(target=pso_constriction_search, args=(antenna, 10.0, 12))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
