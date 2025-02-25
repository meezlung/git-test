# You are in a stronghold, trying to find the End Portal. Unfortunately, you came unprepared, and all you have is a golden pickaxe that can mine one block.

# The stronghold is represented as an r×c grid with the following characters:
    # a space character for empty space (inside a room or a corridor)
    # # for a wall (this is the only block in our scenario)
    # X for the End Portal
    # S for your starting location

# Is it possible to reach the end portal? You are not required to use your golden pickaxe.

# Note that you can only go up, down, left or right from your current location cell.

from collections import deque

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

    if start is None or end is None:
        return False
    
    queue: deque[tuple[int, int, int]] = deque()
    queue.append((start[0], start[1], False)) # queue the point as root of bfs tree as (curr_row, curr_col, have_used_pickaxe)

    # reference maps for points that have been visited or not
    visited: list[list[list[bool]]] = [[[False for _ in range(2)] for _ in range(c)] for _ in range(r)]
    visited[start[0]][start[1]][0] = True

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        curr_row, curr_col, have_used_pickaxe = queue.popleft() # kung popright, para ka na ring nagstack

        # base case
        if (curr_row, curr_col) == end:
            return True

        for dr, dc in directions:
            new_row, new_col = curr_row + dr, curr_col + dc

            if 0 <= new_row < r and 0 <= new_col < c:
                print(new_grid[new_row][new_col])
                if new_grid[new_row][new_col] == " " or new_grid[new_row][new_col] == "X":
                    if not visited[new_row][new_col][have_used_pickaxe]:
                        visited[new_row][new_col][have_used_pickaxe] = True
                        queue.append((new_row, new_col, have_used_pickaxe))

                elif new_grid[new_row][new_col] == "#":
                    if not have_used_pickaxe and not visited[new_row][new_col][1]:
                        visited[new_row][new_col][1] = True
                        queue.append((new_row, new_col, True))

    print(grid)

    return False


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

assert can_reach_end(13, 13, """\
#############
#   ##  #   #
# X ##  #   #
#   ##  #   #
###### ######
######  #   #
#           #
#   #   #   #
## ##########
#   #   #   #
#         S #
#   #   #   #
#############
""") is False

assert can_reach_end(13, 13, """\
#############
#   ##  #   #
# X ##  #   #
#   ##  #   #
# #### ######
# ####  #   #
#           #
#   #   #   #
## ##########
#   #   #   #
#         S #
#   #   #   #
#############
""") is True

assert can_reach_end(13, 13, """\
#############
#   ##  #   #
# X ##  #   #
#   ##  #   #
# #### ######
######  #   #
#           #
#   #   #   #
## ##########
#   #   #   #
#         S #
#   #   #   #
#############
""") is True


