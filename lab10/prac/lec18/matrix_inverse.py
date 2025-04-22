from fractions import Fraction

def invert_matrix(matrix):
    """
    Compute the inverse of a square matrix using Gaussian elimination.

    Args:
        matrix (list of list of floats): A square matrix (n x n).

    Returns:
        list of list of floats: The inverse of the input matrix.

    Raises:
        ValueError: If the matrix is not square or is singular (non-invertible).
    """
    # Number of rows
    n = len(matrix)
    # Check if matrix is square
    if any(len(row) != n for row in matrix):
        raise ValueError("Only square matrices can be inverted")

    # Create an augmented matrix [A | I]
    # Make a deep copy of A and append identity matrix
    
    augmented = [[Fraction(value) for value in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)] # if want to use fractions

    # augmented = [row[:] + [float(i == j) for j in range(n)] for i, row in enumerate(matrix)] # if want to us e floats

    # Perform Gaussian elimination
    for i in range(n):
        # Find pivot element
        pivot = augmented[i][i]
        if abs(pivot) < 1e-12:
            # Pivot is too small, try to swap with a lower row
            swap_row = next((r for r in range(i+1, n) if abs(augmented[r][i]) > 1e-12), None)
            if swap_row is None:
                raise ValueError("Matrix is singular and cannot be inverted.")
            # Swap rows
            augmented[i], augmented[swap_row] = augmented[swap_row], augmented[i]
            pivot = augmented[i][i]

        # Normalize pivot row
        augmented[i] = [value / pivot for value in augmented[i]]

        # Eliminate current column entries in other rows
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                augmented[j] = [augmented[j][k] - factor * augmented[i][k] for k in range(2*n)]

    # Extract the right half as the inverse
    inverse = [row[n:] for row in augmented]
    return inverse


def determinant(matrix):
    """
    Compute the determinant of a square matrix using Gaussian elimination with fractions.

    Args:
        matrix (list of list of numbers): A square matrix (n x n).

    Returns:
        Fraction: The determinant of the input matrix.

    Raises:
        ValueError: If the matrix is not square.
    """
    # Number of rows
    n = len(matrix)
    # Check if matrix is square
    if any(len(row) != n for row in matrix):
        raise ValueError("Only square matrices have determinants")

    # Copy matrix into Fraction type
    A = [[Fraction(value) for value in row] for row in matrix]
    det = Fraction(1)

    # Perform Gaussian elimination to upper-triangular form
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            # Try to swap with a lower row
            swap_row = next((r for r in range(i+1, n) if A[r][i] != 0), None)
            if swap_row is None:
                return Fraction(0)
            A[i], A[swap_row] = A[swap_row], A[i]
            det *= -1  # row swap flips sign
            pivot = A[i][i]

        det *= pivot
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]

    return det


# Example usage:
if __name__ == "__main__":
    A = [[4, 7], [2, 6]]
    
    print(f"det(A) = {determinant(A)}")

    invA = invert_matrix(A)
    print("Inverse of A is:")
    for row in invA:
        print(row)

    
