from collections import deque
import heapq

def fastest_resilience(n_0: int) -> int:
    if n_0 <= 0:
        return 0
    
    # crazy hack: early finish check before BFS
    s = n_0
    while s:
        d = s%10
        if d*d >= n_0:
            return 1
        s//=10

    queue = deque()
    queue.append(n_0) 
    
    dist = {n_0: 0}

    # bfs kinda thing
    while queue:
        n = queue.popleft()
        moves = dist[n]

        s = n
        seen_digits = 0
        while s:
            d = s % 10
            s //= 10
            if d == 0:
                continue
            if (seen_digits >> d) & 1:
                continue
            seen_digits |= 1 << d

            if d * d >= n:  # can finish
                return moves + 1
            
            next_digit = n - d*d
            if next_digit not in dist:
                dist[next_digit] = moves + 1
                queue.append(next_digit)
    # i think this is impossible na

print(fastest_resilience(13))
print(fastest_resilience(98))
print(fastest_resilience(214))
print(fastest_resilience(32))
print(fastest_resilience(200000))