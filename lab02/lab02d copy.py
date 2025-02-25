from collections.abc import Sequence
from collections import defaultdict

def dfs(graph: defaultdict[int, list[int]], u: int, goal: int, visited: set[int], allow_trees: bool, rev_idx: dict[int, tuple[int, int]], grid: list[list[str]]):
    if u == goal:
        return True
    
    visited.add(u)

    for v in graph[u]:
        if v not in visited:
            i, j = rev_idx[v]
            if not allow_trees and grid[i][j] == 'T':
                continue # skip trees
            if dfs(graph, v, goal, visited, allow_trees, rev_idx, grid):
                return True
    
    return False

def paths_to_graph(all_paths: list[list[int]]) -> defaultdict[int, list[int]]:
    solution_graph: defaultdict[int, list[int]] = defaultdict(list)
    
    for path in all_paths:
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            solution_graph[u].append(v)
            solution_graph[v].append(u)
            
    return solution_graph

def find_articulation_points(n: int, graph: defaultdict[int, list[int]]):
    vis = [-1]*n
    low = [-1]*n

    time = 0

    def visit(i: int):
        nonlocal time
        assert vis[i] == -1
        vis[i] = time
        time += 1

    artic_pts: list[int] = []

    def dfs(i: int, parent: int | None):
        visit(i)
        low[i] = vis[i]

        is_articulation = False
        children = 0

        for j in graph[i]:
            if vis[j] == -1:
                children += 1
                dfs(j, i)
                low[i] = min(low[i], low[j])

                if low[j] >= vis[i] and parent is not None:
                    is_articulation = True

            elif j != parent:
                low[i] = min(low[i], vis[j])

        if parent is None and children > 1:
            is_articulation = True

        if is_articulation:
            artic_pts.append(i)

    for i in range(n):
        if vis[i] == -1:
            dfs(i, None)

    return artic_pts

def dfs_all_paths(graph: dict[int, list[int]], node: int, goal: int, visited: set[int], path: list[int], all_paths: list[list[int]]):
    if node == goal:
        all_paths.append(path[:])  #store the current path
        return
    
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:  #prevent cycles
            path.append(neighbor)
            dfs_all_paths(graph, neighbor, goal, visited, path, all_paths)
            path.pop()  # Backtrack

    visited.remove(node)  # ALlow other paths to explore this node again

def find_all_paths(graph: dict[int, list[int]], start: int, goal: int) -> list[list[int]]:
    all_paths: list[list[int]] = []
    dfs_all_paths(graph, start, goal, set(), [start], all_paths)
    return all_paths

def need_to_cut(grid: Sequence[str]) -> list[str]:
    new_grid = [list(row) for row in grid]
    r, c = len(new_grid), len(new_grid[0])

    # locate A and G
    start, goal = None, None
    for i in range(r):
        for j in range(c):
            if grid[i][j] == 'A':
                start = (i, j)
            elif grid[i][j] == 'G':
                goal = (i, j)

    assert start != None and goal != None

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # convert grid into graph
    graph: defaultdict[int, list[int]] = defaultdict(list)
    node_idx: dict[tuple[int, int], int] = {}
    rev_idx: dict[int, tuple[int, int]] = {}
    node_count = 0
    tree_pts: list[tuple[int, int]] = []

    for i in range(r):
        for j in range(c):
            if grid[i][j] in {'.', 'T', 'A', 'G'}:
                node_idx[(i, j)] = node_count
                rev_idx[node_count] = (i, j)
                node_count += 1

                if grid[i][j] == 'T':
                    tree_pts.append((i, j))

    #build adjacency list
    for (i, j), u in node_idx.items():
        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if (ni, nj) in node_idx:
                v = node_idx[(ni, nj)]
                graph[u].append(v)
                # graph[v].append(u)


    # make sure there's a path from A to G first, path with no trees cut, and with trees cut (using dfs)
    start_idx = node_idx[start]
    goal_idx = node_idx[goal]
    
    # make sure to edge case those that have a path alr
    without_trees = dfs(graph, start_idx, goal_idx, visited=set(), allow_trees=False, rev_idx=rev_idx, grid=new_grid) 
    with_trees = dfs(graph, start_idx, goal_idx, visited=set(), allow_trees=True, rev_idx=rev_idx, grid=new_grid)
        
    if not without_trees and not with_trees:
        return ["".join(row) for row in grid]
    
    if without_trees:
        return ["".join(row) for row in grid]


    all_paths = find_all_paths(graph, start_idx, goal_idx)
    solution_graph = paths_to_graph(all_paths)

    artic_points = find_articulation_points(len(node_idx), solution_graph)
    for artc in artic_points:
        i, j = rev_idx[artc]
        if (i, j) in tree_pts:
            new_grid[i][j] = "*"

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