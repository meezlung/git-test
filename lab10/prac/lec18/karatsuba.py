def karatsuba_int(x: int, y: int) -> int:
    """
    Multiply two non-negative integers using Karatsuba algorithm.
    """
    # Base case for small numbers
    if x < 10 or y < 10:
        return x * y

    # Compute the number of digits of the largest input
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # Split x and y
    high_x, low_x = divmod(x, 10 ** half)
    high_y, low_y = divmod(y, 10 ** half)

    # Three recursive multiplications
    z0 = karatsuba_int(low_x, low_y)
    z2 = karatsuba_int(high_x, high_y)
    z1 = karatsuba_int(low_x + high_x, low_y + high_y) - z2 - z0

    # Combine results
    return (z2 * 10 ** (2 * half)) + (z1 * 10 ** half) + z0


def karatsuba_poly(p: list[int], q: list[int]) -> list[int]:
    """
    Multiply two polynomials p and q using Karatsuba's algorithm.
    Polynomials are lists of coefficients from lowest to highest degree.
    """
    # Ensure p and q have same length by padding with zeros
    n = max(len(p), len(q))
    if n == 0:
        return []
    if n == 1:
        return [p[0] * q[0]]

    # Next power of two or half size
    m = (n + 1) // 2 # ceil(n / 2)

    # Split p and q into low and high parts
    p_low = p[:m]
    p_high = p[m:]
    q_low = q[:m]
    q_high = q[m:]

    print(p_low) 
    print(p_high)
    print(q_low) 
    print(q_high)
    print()

    # Pad splits to length m and n-m
    p_low += [0] * (m - len(p_low))
    p_high += [0] * (n - m - len(p_high))
    q_low += [0] * (m - len(q_low))
    q_high += [0] * (n - m - len(q_high))

    print(p_low) 
    print(p_high)
    print(q_low) 
    print(q_high)
    print()

    # Recursive multiplications
    z0 = karatsuba_poly(p_low, q_low)
    z2 = karatsuba_poly(p_high, q_high)

    # sum_p = p_low + p_high, sum_q = q_low + q_high
    len_sum_p = max(len(p_low), len(p_high))
    sum_p = [(p_low[i] if i < len(p_low) else 0) + (p_high[i] if i < len(p_high) else 0)
             for i in range(len_sum_p)]
    len_sum_q = max(len(q_low), len(q_high))
    sum_q = [(q_low[i] if i < len(q_low) else 0) + (q_high[i] if i < len(q_high) else 0)
             for i in range(len_sum_q)]
    z1 = karatsuba_poly(sum_p, sum_q)

    # z1 = z1 - z2 - z0 (pad z1 to adequate length)
    k = max(len(z1), len(z0), len(z2))
    z1 += [0] * (k - len(z1))
    for i in range(len(z0)):
        z1[i] -= z0[i]
    for i in range(len(z2)):
        z1[i] -= z2[i]

    # Assemble result of size len(p)+len(q)-1
    result_size = len(p) + len(q) - 1
    result = [0] * result_size

    # Add z0
    for i, v in enumerate(z0):
        result[i] += v
    # Add z1 shifted by m
    for i, v in enumerate(z1):
        if i + m < result_size:
            result[i + m] += v
    # Add z2 shifted by 2*m
    for i, v in enumerate(z2):
        if i + 2 * m < result_size:
            result[i + 2 * m] += v

    # Trim trailing zeros
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


if __name__ == "__main__":
    # Examples for integer multiplication
    print("Karatsuba int 31415926 * 27182818:", karatsuba_int(31415926, 27182818))
    # Examples for polynomial multiplication
    # p = [3, 1, 4]  # 4x^2 + 1x + 3
    # q = [9, 5, 1]  # 1x^2 + 5x + 9
    # print("Karatsuba poly [3,1,4] * [9,5,1]:", karatsuba_poly(p, q))
    
    p = [1, -2, 2]
    q = [1, -2, 2]
    print("Karatsuba poly [1, -2, 2] * [1, -2, 2]:", karatsuba_poly(p, q))
