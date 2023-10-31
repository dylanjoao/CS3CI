from random import shuffle
import pandas as pd
import math
import copy

class TSP:

    def __init__(self, matrix):
        self.matrix = matrix

    def is_valid(self, tour):
        number_of_cities = len(self.matrix[0])

        # Check for duplicates and within range
        sorted_tour = copy.deepcopy(tour)
        sorted_tour.sort()
        for i in range(len(sorted_tour)):
            if i != len(sorted_tour)-1:
                if sorted_tour[i] == sorted_tour[i + 1]:
                    return False
            if sorted_tour[i] > len(sorted_tour)-1:
                return False
            elif sorted_tour[i] < 0:
                return False

        return True

    def evaluate_route(self, route):
        cost = 0
        last = 0
        for i in range(len(self.matrix[0])):
            current = route[i]
            cost += self.matrix[last][current]
            last = current

        cost += self.matrix[last][0]

        return cost

    def random_route(self):
        route = []

        for i in range(len(self.matrix[0])):
            route.append(i)

        shuffle(route)
        return route

    def matrix_from_csv(self, file):
        df = pd.read_csv(file)
        self.matrix =  [ [0] * len(df) for _ in range(len(df))]

        for i in range(len(df)):
            for j in range(len(df)):
                row = df.iloc[i]
                row2 = df.iloc[j]

                distance = math.sqrt((row['x'] - row2['x'])**2 + (row['y'] - row2['y'])**2)

                self.matrix[i][j] = distance
                self.matrix[j][i] = distance

