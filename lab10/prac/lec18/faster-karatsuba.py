def karatsuba_pv(x: int, y: int, base: int = 10) -> int:
    """
    Multiply x*y by splitting each into (a·B + b) and
    doing only three recursive calls at x=0,1,-1, then
    interpolating via the formulas

      r0    = r(0)
      r1    = ( r(1) – r(–1) ) / 2
      r2    = ( r(1) + r(–1) ) / 2 – r(0)

    before recombining as r2·B² + r1·B + r0.
    """
    # cutoff to schoolbook
    if x < base or y < base:
        return x * y

    # split position: half the digits in 'base'
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    B = base ** m

    # split x = a·B + b,  y = c·B + d
    a, b = divmod(x, B)
    c, d = divmod(y, B)

    # 1) compute the three point‐values recursively
    r0    = karatsuba_pv(b, d, base)            # r(0)   = b·d
    r1    = karatsuba_pv(a + b, c + d, base)    # r(1)   = (a+b)(c+d)
    r_neg = karatsuba_pv(b - a, d - c, base)    # r(–1)  = (–a+b)(–c+d) = (b–a)(d–c)

    # 2) interpolate to get coefficients r2, r1_coeff, r0
    #    (all divisions are exact in integers)
    coef_r2 = (r1 + r_neg) // 2 - r0
    coef_r1 = (r1 - r_neg) // 2
    coef_r0 = r0

    # 3) recombine into the final integer
    return coef_r2 * B * B + coef_r1 * B + coef_r0

if __name__ == "__main__":
    # Example 1: small numbers
    x1, y1 = 1234, 5678
    print(f"{x1} × {y1} = {karatsuba_pv(x1, y1)}")  
    # Output: 1234 × 5678 = 7006652

    # Example 2: larger numbers
    x2 = 3141592653589793
    y2 = 2718281828459045
    result = karatsuba_pv(x2, y2)
    print(f"{x2} × {y2} = {result}")
    # Verify correctness
    assert result == x2 * y2