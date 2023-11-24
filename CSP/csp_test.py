array_2d = [[(0, 2, 0), (1, 1, 0)], [(1, 2, 0), (0, 2, 1), (1, 0, 2)], [(2, 0, 2)]]

max_length = max(len(sub_array) for sub_array in array_2d)
sums = [0] * max_length

for sub_array in array_2d:
    for i, element in enumerate(sub_array):
        for j, value in enumerate(element):
            sums[j] += value

# Print the results
for i, total in enumerate(sums):
    print(f"Sum of nth elements at index {i}: {total}")

print(max_length)
print(sums)