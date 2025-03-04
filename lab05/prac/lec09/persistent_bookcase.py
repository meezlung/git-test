# type: ignore

import sys
import copy

def solve():
    # Read input
    n, m, q = map(int, sys.stdin.readline().split())

    # Persistent storage of book states
    state: list[set[int]] = [set()]  # Initial empty state
    operation_map = {0: 0}  # Maps operation index to state version

    results = []
    
    for op_id in range(1, q + 1):
        line = sys.stdin.readline().split()
        op_type = int(line[0])

        # Clone the previous state
        new_state = copy.deepcopy(state[-1])

        if op_type == 1:  # Place a book
            i, j = map(int, line[1:])
            new_state.add((i, j))
        elif op_type == 2:  # Remove a book
            i, j = map(int, line[1:])
            new_state.discard((i, j))
        elif op_type == 3:  # Invert a shelf
            i = int(line[1])
            to_flip = {(i, j) for j in range(1, m + 1)}
            new_state.symmetric_difference_update(to_flip)
        elif op_type == 4:  # Restore to k-th state
            k = int(line[1])
            new_state = state[operation_map[k]]  # Directly use past version

        # Store new state and map operation to it
        state.append(new_state)
        operation_map[op_id] = len(state) - 1

        # Store result (number of books)
        results.append(str(len(new_state)))

    # Print all results at once for efficiency
    sys.stdout.write("\n".join(results) + "\n")


solve()