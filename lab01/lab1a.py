from collections.abc import Sequence
from heapq import heappop, heappush

def min_ladders(mountain: Sequence[Sequence[int]]) -> int:

    ans  = 0
    visited:set[tuple[int,int]] = set()
    r = len(mountain)
    c = len(mountain[0])

    pq:list[tuple[int,...]] = []

    z  = mountain[0][0]

    heappush(pq, (0,z,0,0)) # cost,nod_val,x,y
    
    dir_:list[tuple[int,int]] = [(1,0),(-1,0),(0,1),(0,-1)] #

    while pq:
        cost,i, x,y = heappop(pq)

        if (x,y) in visited:
            continue

        visited.add((x,y))
        ans += cost

        for dx,dy in dir_:

            nx, ny = dx+x,dy+y

            if 0 <= nx < r and 0 <= ny < c: # bounds check
                
                j = mountain[nx][ny]
                if i < j or i> j:
                    heappush(pq, (abs(j-i),j,nx,ny))

                elif i == j:
                    heappush(pq,(0,j,nx,ny))
    
    return ans




