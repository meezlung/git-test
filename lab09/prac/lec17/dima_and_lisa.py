# type: ignore

import math

def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(x)) + 1, 2):
        if x % i == 0:
            return False
    return True

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    
    if is_prime(n):
        print(1)
        print(n)
    elif is_prime(n - 2):
        print(2)
        print(2, n - 2)
    else:
        print(3)
        print(2, 2, n - 4)

if __name__ == '__main__':
    solve()
