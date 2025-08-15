# Kevin the Villager challenges you to a game.

# There are n colors of wool numbered 1 to n, and you have exactly 2 blocks of each color. There are m pillars numbered 1 to m, and pillar i contains p[i] blocks of wool.

# Your goal is to obtain all 2n blocks of wool. You're only allowed to accomplish this via moves.

# Each move is as follows:

# Choose two pillars i and j (1≤i<j≤m), and get the blocks of wool on top of these two pillars.
# You may only do this if the two blocks of wool on top are of the same color.

# Can you win?

from collections import defaultdict, deque

def winnable(n: int, pillars: list[list[int]]) -> bool:
    stacks = [pillar for pillar in pillars] # reverse pillars each pillar is given in order from bottom to top

    top_colors_of_pillars: dict[int, set[int]] = defaultdict(set)
    ready_to_match: deque[int] = deque()

    for i, stack in enumerate(stacks):
        if stack:
            top_color = stack[-1]
            top_colors_of_pillars[top_color].add(i)
            if len(top_colors_of_pillars[top_color]) == 2:
                ready_to_match.append(top_color)

    print("stacks", stacks)
    print("top_colors", top_colors_of_pillars)
    print("ready_to_match", ready_to_match)

    while ready_to_match:
        color = ready_to_match.popleft()
        p = list(top_colors_of_pillars[color])

        # print("top_colors", top_colors_of_pillars)

        print(p)

        # remove again top blocks
        for pillar in p:
            stacks[pillar].pop()
            top_colors_of_pillars[color].remove(pillar)
            print("top_colors2", top_colors_of_pillars)


            # update the map na
            if stacks[pillar]:
                new_top = stacks[pillar][-1]
                top_colors_of_pillars[new_top].add(pillar)
                print("top_colors3", top_colors_of_pillars)


                if len(top_colors_of_pillars[new_top]) == 2:
                    ready_to_match.append(new_top)

        if not top_colors_of_pillars[color]:
            del top_colors_of_pillars[color]

        print(ready_to_match)

    return all(len(stack) == 0 for stack in stacks)


print(winnable(2, [[1, 2], [1, 2]]))
print()
print(winnable(2, [[1, 2], [2, 1]]))
print()

print(winnable(3, [[1, 2, 3], [1, 2], [3]]))
print()

print(winnable(3, [[3, 2, 1], [1, 2], [3]]))
print()

print(winnable(3, [[3], [1, 2, 3], [1, 2]]))
print()

print(winnable(3, [[1, 2, 3], [3], [1, 2]]))
print()

print(winnable(4, [[4], [3, 4], [1, 2, 3], [1, 2]]))
print()


assert winnable(2, [[1, 2], [1, 2]]) is True
assert winnable(2, [[1, 2], [2, 1]]) is False
assert winnable(1, [[1, 1]]) is False

    
