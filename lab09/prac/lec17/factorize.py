# type: ignore

from math import gcd
from random import randrange

def find_factor(n):
    f = lambda x: (x**2 + 1) % n
    a = randrange(n)

    tortoise = hare = a
    while True:
        tortoise = f(tortoise)
        hare = f(f(hare))

        # did we cycle?
        if (g := gcd(tortoise - hare, n)) > 1:
            return g
