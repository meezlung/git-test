# You are in a stronghold, trying to find the End Portal. Unfortunately, you came unprepared, and all you have is a golden pickaxe that can mine one block.

# The stronghold is represented as an r×c grid with the following characters:
    # a space character for empty space (inside a room or a corridor)
    # # for a wall (this is the only block in our scenario)
    # X for the End Portal
    # S for your starting location

# Is it possible to reach the end portal? You are not required to use your golden pickaxe.

# Note that you can only go up, down, left or right from your current location cell.

def solve(x: int, y: int, r: int, c: int, grid: list[list[str]], path: list[tuple[int, int]], visited: set[tuple[int, int]]) -> bool:
    # base case
    if y < 0 or y >= r or x < 0 or x >= c:
        return False
    
    if grid[y][x] == "X":
        path.append((x, y))
        return True
    
    if grid[y][x] == "#":
        return False

    if grid[y][x] != " " and grid[y][x] != "S":
        return False
    
    # mark the current cell as visited
    visited.add((x, y))
    path.append((x, y))

    # recursive case
    if (x + 1, y) not in visited:
        if solve(x + 1, y, r, c, grid, path, visited): # right
            return True

    if (x, y + 1) not in visited:
        if solve(x, y + 1, r, c, grid, path, visited): # down
            return True

    if (x - 1, y) not in visited:
        if solve(x - 1, y, r, c, grid, path, visited): # left
            return True
    
    if (x, y - 1) not in visited:
        if solve(x, y - 1, r, c, grid, path, visited): # up
            return True
    
    # backtracking
    path.pop()
    visited.remove((x, y))
    return False

def can_reach_end(r: int, c: int, grid: str) -> bool:
    new_grid = [list(row) for row in grid.split("\n")]
    path: list[tuple[int, int]] = []

    # find the starting position
    start_x = start_y = -1
    for i in range(r):
        for j in range(c):
            if new_grid[i][j] == "S":
                start_x, start_y = j, i
                break
        if start_x != -1:
            break

    for row in new_grid:
        print("".join(row))

    print(start_x, start_y)

    result = solve(start_x, start_y, r, c, new_grid, path, set())

    print(result)
    return result


assert can_reach_end(13, 13, """\
#############
#   #   #   #
# X #   #   #
#   #   #   #
###### ######
#   #   #   #
#           #
#   #   #   #
## ##########
#   #   #   #
#         S #
#   #   #   #
#############
""") is True

