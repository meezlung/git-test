def next_tea_party(m: int, n: int, s: int) -> int:
    # Define the periodicities (in microseconds)
    p1 = 4455204553
    p2 = 8291419363
    p3 = 49356059989
    
    # Compute the remainders: 
    # T + m must be a multiple of p1, so T ≡ -m (mod p1), etc.
    a1 = (-m) % p1
    a2 = (-n) % p2
    a3 = (-s) % p3

    # Compute the total product (the modulus for the CRT)
    N = p1 * p2 * p3
    
    # Helper function: extended Euclidean algorithm to compute modular inverses.
    def modinv(a: int, mod: int) -> int:
        # extended Euclidean algorithm:
        # returns x such that (a*x) % mod == 1.
        # (Assumes that a and mod are coprime.)
        original_mod = mod
        x0, x1 = 1, 0
        while mod:
            q, a, mod = a // mod, mod, a % mod
            x0, x1 = x1, x0 - q * x1
        # x0 is the inverse mod original_mod.
        return x0 % original_mod
    
    # Compute individual contributions:
    N1 = N // p1  # N/p1
    N2 = N // p2  # N/p2
    N3 = N // p3  # N/p3
    
    # Compute their modular inverses modulo the corresponding prime (assumed coprime)
    M1 = modinv(N1, p1)
    M2 = modinv(N2, p2)
    M3 = modinv(N3, p3)
    
    # Combine using the CRT formula:
    T = (a1 * M1 * N1 + a2 * M2 * N2 + a3 * M3 * N3) % N
    
    # Return T. 
    # If by design T==0 should correspond to waiting a full period,
    # then the check would be: if T == 0: return N, else return T.
    # Here we assume that T==0 means "available now".
    return T

# # Example usage:
# if __name__ == '__main__':
#     # Example provided:
#     result = next_tea_party(4455204520, 8291419330, 49356059956)
#     print(result)  # Expected output: 33
