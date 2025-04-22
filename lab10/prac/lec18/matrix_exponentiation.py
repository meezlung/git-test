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
