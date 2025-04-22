def naive_mat_mult(A, B):
    """
    Perform standard matrix multiplication (A @ B).
    A is an m×n matrix, B is an n×p matrix. Returns m×p matrix.
    """
    m, n = len(A), len(A[0])
    # assume B has dimensions n x p
    p = len(B[0])
    # initialize result
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for k in range(n):
            for j in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C


def _add_matrix(A, B):
    """Elementwise addition of two same-size matrices."""
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def _sub_matrix(A, B):
    """Elementwise subtraction of two same-size matrices."""
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def _split_matrix(M):
    """Split a square matrix M of size n into quadrants."""
    n = len(M)
    mid = n // 2
    A11 = [row[:mid] for row in M[:mid]]
    A12 = [row[mid:] for row in M[:mid]]
    A21 = [row[:mid] for row in M[mid:]]
    A22 = [row[mid:] for row in M[mid:]]
    return A11, A12, A21, A22


def _combine_quadrants(C11, C12, C21, C22):
    """Combine four quadrants into one matrix."""
    top = [c11 + c12 for c11, c12 in zip(C11, C12)]
    bottom = [c21 + c22 for c21, c22 in zip(C21, C22)]
    return top + bottom


def strassen(A, B, threshold=64):
    """
    Multiply two square matrices A and B using Strassen's algorithm.
    threshold: switch to naive multiplication when size <= threshold.
    """
    # Ensure square
    n = len(A)
    if n <= threshold:
        return naive_mat_mult(A, B)

    # If n is odd, pad to next even
    if n % 2 != 0:
        # pad A and B to size n+1
        A = [row + [0] for row in A] + [[0] * (n+1)]
        B = [row + [0] for row in B] + [[0] * (n+1)]
        n += 1

    # Split into quadrants
    A11, A12, A21, A22 = _split_matrix(A)
    B11, B12, B21, B22 = _split_matrix(B)

    # Compute Strassen's 7 products
    M1 = strassen(_add_matrix(A11, A22), _add_matrix(B11, B22), threshold)
    M2 = strassen(_add_matrix(A21, A22), B11, threshold)
    M3 = strassen(A11, _sub_matrix(B12, B22), threshold)
    M4 = strassen(A22, _sub_matrix(B21, B11), threshold)
    M5 = strassen(_add_matrix(A11, A12), B22, threshold)
    M6 = strassen(_sub_matrix(A21, A11), _add_matrix(B11, B12), threshold)
    M7 = strassen(_sub_matrix(A12, A22), _add_matrix(B21, B22), threshold)

    # Compute result quadrants
    C11 = _add_matrix(_sub_matrix(_add_matrix(M1, M4), M5), M7)
    C12 = _add_matrix(M3, M5)
    C21 = _add_matrix(M2, M4)
    C22 = _add_matrix(_sub_matrix(_add_matrix(M1, M3), M2), M6)

    # Combine quadrants
    C = _combine_quadrants(C11, C12, C21, C22)

    # If we padded, trim back to original size
    return [row[:len(B[0]) if n%2==0 else n-1] for row in (C[:len(A) if n%2==0 else n-1])]  

def identity_matrix(n):
    """Return the n×n identity matrix."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def mat_pow(A, exponent, multiply=naive_mat_mult):
    """
    Compute A^exponent using fast (binary) exponentiation.
    
    A: square n×n matrix (list of lists)
    exponent: non-negative integer power
    multiply: function f(X, Y) -> X×Y (both n×n), defaults to naive_mat_mult
    
    Returns the n×n matrix A^exponent.
    """
    if exponent < 0:
        raise ValueError("This function does not support negative exponents.")
    n = len(A)
    # check square
    if any(len(row) != n for row in A):
        raise ValueError("mat_pow: A must be square")
    
    result = identity_matrix(n)
    base = A
    
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    
    return result

# Example usage
if __name__ == "__main__":
    A = [
        [2, 1],
        [1, 0]
    ]
    # Compute Fibonacci numbers via matrix power:
    # [F_{k+1}  F_k  ] = [2 1;1 0]^k
    for k in range(6):
        M = mat_pow(A, k)
        print(f"A^{k} =", M)

# Example usage
if __name__ == "__main__":
    A = [[1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10,11,12],
         [13,14,15,16]]
    B = [[16,15,14,13],
         [12,11,10, 9],
         [8, 7, 6, 5],
         [4, 3, 2, 1]]
    print("Naive multiply:", naive_mat_mult(A, B))
    print("Strassen multiply:", strassen(A, B))
