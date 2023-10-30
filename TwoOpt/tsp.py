from random import shuffle
import pandas as pd
import math

class TSP:

    def __init__(self, matrix):
        self.matrix = matrix

    def is_valid(self, tour):
        pass

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

