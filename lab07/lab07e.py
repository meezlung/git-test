# type: ignore
from layton import ask_layton

def solve_puzzle(s: str) -> list[int]:
    n = len(s)
    r = s[::-1]
    t = s + "#" + r
    ask_t = ask_layton(t)
    return [2 * ask_t(i, 2 * n - i) - 1 for i in range(n)]