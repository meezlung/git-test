from collections import deque

def is_within_bounds(new_row: int, new_col: int, r: int, c: int):
    return 0 <= new_row < r and 0 <= new_col < c

def can_reach_end(r: int, c: int, grid: str) -> bool:
    new_grid = [list(row) for row in grid.split("\n") if row]
    start = None
    end = None

    for i in range(r):
        for j in range(c):
            if new_grid[i][j] == "S":
                start = (i, j)
            elif new_grid[i][j] == "X":
                end = (i, j)

    if start is None or end is None: # most likely not
        return False
    
    # initialize bfs
    queue: deque[tuple[int, int, int]] = deque() # elements of tuple: (curr row, curr col, have_used_pickaxe)
    queue.append((start[0], start[1], False))

    # make an empty template for the visiteds
    visited: list[list[list[bool]]] = [[[False for _ in range(2)] for _ in range(c)] for _ in range(r)]

    visited[start[0]][start[1]][0] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        curr_row, curr_col, have_used_pickaxe = queue.popleft()
        # base case
        if (curr_row, curr_col) == end:
            return True

        for dr, dc in directions:
            new_row, new_col = curr_row + dr, curr_col + dc
            if is_within_bounds(new_row, new_col, r, c):
                if new_grid[new_row][new_col] == " " or new_grid[new_row][new_col] == "X":
                    if not visited[new_row][new_col][have_used_pickaxe]:
                        visited[new_row][new_col][have_used_pickaxe] = True
                        queue.append((new_row, new_col, have_used_pickaxe))
                        
                elif new_grid[new_row][new_col] == "#":
                    if not have_used_pickaxe and not visited[new_row][new_col][1]:
                        visited[new_row][new_col][1] = True
                        queue.append((new_row, new_col, True))
    return False