# type: ignore

from collections.abc import Sequence
Edge = tuple[int, int]
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def is_valid(grid, r, c, ni, nj):
    return 0 <= ni < r and 0 <= nj < c and grid[ni][nj] != '#'

def find(r, c, grid):
    start = (-1, -1)
    end = (-1, -1)
    for i in range(0, r, 2):
        for j in range(0, c, 2):
            cell = grid[i][j]
            if cell == 'A':
                start = (i, j)
            elif cell == 'G':
                end = (i, j)
    return start, end

def need_to_cut(grid):
    r, c = len(grid), len(grid[0])
    start, end = find(r, c, grid)
    time = 0
    low = {}
    vis = {(i, j): -1 for i in range(r) for j in range(c)}
    articulation = []

    def visit(i, j) -> None:
        nonlocal time
        vis[(i, j)] = time
        time += 1

    def dfs(cell: Edge, parent_cell: Edge | None) -> bool:
        visit(*cell)  
        low[cell] = vis[cell]
        children = 0
        subtree_end = cell == end  
        if cell == start or cell == end: 
            for dx, dy in directions:
                neigh = (cell[0] + dx, cell[1] + dy)
                if not is_valid(grid, r, c, *neigh) or neigh == parent_cell:
                    continue

                if vis[neigh] == -1:
                    children += 1
                    child_end = dfs(neigh, cell)
                    if not subtree_end and child_end:
                        subtree_end = True 

                    low[cell] = min(low[cell], low[neigh])

                    if parent_cell is not None: 
                        if low[neigh] >= vis[cell] and child_end:
                            if grid[cell[0]][cell[1]] == 'T': 
                                articulation.append(cell)

                else:
                    low[cell] = min(low[cell], vis[neigh])

            if parent_cell is None and children > 1 and subtree_end:
                if grid[cell[0]][cell[1]] == 'T':
                    articulation.append(cell)

        else:  
            for dx, dy in directions:
                neigh = (cell[0] + dx, cell[1] + dy)
                if not is_valid(grid, r, c, *neigh) or neigh == parent_cell:
                    continue

                if vis[neigh] == -1:
                    children += 1
                    child_end = dfs(neigh, cell)
                    if not subtree_end and child_end:
                        subtree_end = True 

                    low[cell] = min(low[cell], low[neigh])

                    if parent_cell is not None: 
                        if low[neigh] >= vis[cell] and child_end:
                            if grid[cell[0]][cell[1]] == 'T':  
                                articulation.append(cell)
                else:
                    low[cell] = min(low[cell], vis[neigh])  

        if parent_cell is None and children > 1 and subtree_end:
            if grid[cell[0]][cell[1]] == 'T':  
                articulation.append(cell)

        return subtree_end  
    
    dfs(start, None)
    new_grid = [list(row) for row in grid]
    for i, j in articulation:
        new_grid[i][j] = '*'
    return ["".join(row) for row in new_grid]


for c in need_to_cut("""\
G.#
T.T
A##
""".splitlines()):
    print(c)

print()


for c in need_to_cut("""\
G..
T#.
AT.
""".splitlines()):
    print(c)

print()


for c in need_to_cut("""\
.#G
T#T
A..
""".splitlines()):
    print(c)

print()

for c in need_to_cut("""\
.T.T..G......
############.
.........#.#.
T#T#T#T#T#T#.
.#.#.#.#.#.#.
T#.#.#.#.#T#.
.#.#.#.#.#.#.
T#T#T###T#T#T
.#.#.........
##.##########
......A..T.T.
""".splitlines()):
    print(c)

print()

for c in need_to_cut("""\
......G......
T#T#T#.#T#T#.
.............
.#T#T#T#T#T#T
.............
T#T#T#T#T#T#.
.............
.#T#T#T#T#T#T
.............
T#T#T#T#T#T#.
......A......
""".splitlines()):
    print(c)

print()

for c in need_to_cut("""\
......G......
T#T#T#T#T#T#T
.............
#############
.T.T.T.T.T.T.
T#T#T#T#T#T#T
.T.T.T.T.T.T.
T#T#T#T#T#T#T
.T.T.T.T.T.T.
T#T#T#T#T#T#T
.T.T.TAT.T.T.
""".splitlines()):
    print(c)