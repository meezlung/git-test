from functools import lru_cache

# Allowed “crossings” between boundary states 0–8
allowed_transitions = {
    (0,0), (0,2), (2,1), (0,8), (0,7), (7,1),
    (1,1), (1,4), (4,0),
    (2,4), (3,6), (4,5), (4,7), (4,8),
    (4,2), (6,3), (5,4), (7,4), (8,4)
}

MOD = 10**8

@lru_cache(None)
def t(inp, out, width):
    if width == 1:
        return int((inp, out) in allowed_transitions)
    half = width // 2
    total = 0
    for mid in range(8):  # combine on intermediate state mid = 0..7
        total = (total + t(inp, mid, half) * t(mid, out, width - half)) % MOD
    return total

# T(10^12) is t(4,8,10^12)
print(t(4, 8, 10**12))
