def num_defeated(u: int, v: int, w: int, x: int) -> tuple[tuple[int, int, int], tuple[int, int, int]] | None:
    # Helper: standard extended gcd for two numbers.
    def egcd(a: int, b: int) -> tuple[int, int, int]:
        if b == 0:
            return (a, 1, 0)
        else:
            g, x1, y1 = egcd(b, a % b)
            return (g, y1, x1 - (a // b) * y1)
    
    # First compute gcd(u,v,w) and obtain a nontrivial representation.
    # Compute extended gcd for u and v.
    g1, x1, y1 = egcd(u, v)
    # Now combine with w:
    # We want: A*g1 + Z*w = g, where g = gcd(g1, w)
    g, A, Z = egcd(g1, w)
    
    # g is the gcd(u,v,w)
    if g >= x:  # Impossible because the difference must be < x.
        return None
    
    # The combination for u, v, w is now:
    #   u*(x1*A) + v*(y1*A) + w*Z = g
    X, Y, Z = x1 * A, y1 * A, Z

    # At this point (X, Y, Z) might contain negative components.
    # To build nonnegative solutions for the two players,
    # we "shift" by a common amount M.
    M = max(0, -min(X, Y, Z))
    
    # Neru's counts and Alice's counts: Their difference is (X, Y, Z).
    neru = (M + X, M + Y, M + Z)
    alice = (M, M, M)
    
    return (neru, alice)


# # --- Example Testcases ---
# if __name__ == '__main__':
#     # Example 1:
#     result1 = num_defeated(1, 2, 3, 10)
#     print("Example 1 Result:", result1)
#     # Example 2:
#     result2 = num_defeated(20, 15, 10, 5)
#     print("Example 2 Result:", result2)
