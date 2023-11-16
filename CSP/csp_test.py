import itertools


def generate_combinations(arr):
    result = []
    length = len(arr)
    patterns = []

    for i in range(length):
        combinations = []
        for j in range(arr[i] + 1):
            combinations.append(j)
        result.append(combinations)

    for combination in itertools.product(*result):
        patterns.append(combination)

    return patterns


# Example usage:
arr = [2, 2, 1]
combinations = generate_combinations(arr)

print(combinations)