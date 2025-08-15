def best_rolls(softness_vals: list[int], k: int) -> list[int]:
    n = len(softness_vals)
    if k > n:
        return []

    # Sort the softness values along with their original indices
    indexed_vals = sorted(enumerate(softness_vals), key=lambda x: x[1])
    
    min_variance = float('inf')
    best_indices = []

    # Check each window of size k
    for i in range(n - k + 1):
        diff = indexed_vals[i + k - 1][1] - indexed_vals[i][1]
        if diff < min_variance:
            min_variance = diff
            best_start = i

    return [indexed_vals[j][0] for j in range(best_start, best_start + k)]

print(best_rolls([20, 30, 15, 29, 28], 3))
print(best_rolls([123, 456, 789, 12, 345, 678, 901], 2))