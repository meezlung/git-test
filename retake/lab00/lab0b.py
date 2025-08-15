# from collections import deque

# Coord = tuple[int, int]

# def least_jumps(grid: list[list[int]], d: int, u: int, s: Coord, e: Coord) -> int | None:
#     rows, cols = len(grid), len(grid[0])
#     queue = deque([(s[0], s[1], 0)])  # (row, col, jumps)
#     visited = set()
#     visited.add(s)

#     directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

#     while queue:
#         x, y, jumps = queue.popleft()

#         if (x, y) == e:
#             return jumps

#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
#                 height_diff = abs(grid[nx][ny] - grid[x][y])
#                 if height_diff <= d or height_diff <= u:
#                     visited.add((nx, ny))
#                     queue.append((nx, ny, jumps + 1))

#     return None


from collections import deque

Coord = tuple[int, int]

def least_jumps(grid: list[list[int]], d: int, u: int, s: Coord, e: Coord) -> int|None:
    rows, cols = rows, cols = len(grid), len(grid[0])
    sx, sy = s
    ex, ey = e

    # DP table: minimal jumps to reach each cell
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[sx][sy] = 0 # base case

    queue = deque([(sx, sy)]) 
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    while queue:
        x, y = queue.popleft()
        curd = dist[x][y]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                delta = grid[nx][ny] - grid[x][y]
                allowed = (delta <= u) if delta > 0 else (-delta <= d)
                if not allowed: # new trick is to early exit pog
                    continue

                nd = curd + 1
                if nd < dist[nx][ny]:
                    dist[nx][ny] = nd
                    queue.append((nx, ny))

    return dist[ex][ey] if dist[ex][ey] != float('inf') else None

print(least_jumps([
        [1, 5, 1],
        [3, 5, 5],
        [2, 1, 1],
    ], 1, 2, (0, 0), (2, 2)))

print(least_jumps([
        [1, 5, 1],
        [3, 5, 5],
        [2, 1, 1],
    ], 1, 2, (0, 0), (0, 2)))