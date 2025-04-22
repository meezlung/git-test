def mat_mult(A, B):
    """
    Multiply two square matrices A and B of size k×k.
    """
    k = len(A)
    C = [[0] * k for _ in range(k)]
    for i in range(k):
        for r in range(k):
            a = A[i][r]
            for j in range(k):
                C[i][j] += a * B[r][j]
    return C


def mat_pow(A, power):
    """
    Raise square matrix A to the integer power using fast exponentiation.
    """
    k = len(A)
    # Identity matrix
    result = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    print(result)
    base = [row[:] for row in A] # just make a copy of A
    print(base)
    while power > 0:
        if power & 1:
            result = mat_mult(result, base)
        base = mat_mult(base, base)
        power >>= 1
    return result


def count_no_CS33(n: int) -> int:
    """
    Return the number of length-n strings over {3, S, C} that do NOT contain 'CS33' as a substring.
    Uses a 4-state automaton and matrix exponentiation in O(log n) time.
    """
    # Transition matrix T[i][j] = count of letters sending state i -> state j
    T = [
        [2, 1, 0, 0],  # from state 0
        [1, 1, 1, 0],  # from state 1
        [1, 1, 0, 1],  # from state 2
        [0, 1, 1, 0],  # from state 3
    ]
    # Initial distribution: v(0) = [1,0,0,0]^T (empty string at state 0)
    v0 = [1, 0, 0, 0]

    # Compute T^n
    Tn = mat_pow(T, n)

    # Multiply T^n by v0 to get v(n)
    vn = [sum(v0[j] * Tn[j][i] for j in range(4)) for i in range(4)]

    # Total valid strings = sum of all non-dead states
    return sum(vn)


if __name__ == "__main__":
    for n in [0, 1, 2, 3, 4, 5, 10]:
        print(f"n={n}: {count_no_CS33(n)} valid strings")
        print()

