# Kevin the Villager challenges you to a game.

# There are n colors of wool numbered 1 to n, and you have exactly 2 blocks of each color. There are m pillars numbered 1 to m, and pillar i contains p[i] blocks of wool.

# Your goal is to obtain all 2n blocks of wool. You're only allowed to accomplish this via moves.

# Each move is as follows:

# Choose two pillars i and j (1≤i<j≤m), and get the blocks of wool on top of these two pillars.
# You may only do this if the two blocks of wool on top are of the same color.

# Can you win?

from collections import defaultdict

def winnable(n: int, pillars: list[list[int]]) -> bool:
    stacks = [pillar[::-1] for pillar in pillars] # reverse pillars each pillar is given in order from bottom to top

    print("STACKS BEFORE", stacks)
    
    # to track 
    top_colors_of_pillars: dict[int, list[int]] = defaultdict(list)
    for i, stack in enumerate(stacks):
        print(i, stack)
        if stack:
            top_colors_of_pillars[stack[-1]].append(i) # append index of that pillar with a specific color
                                                       # so that we now know what's the first thing to match
    
    print(top_colors_of_pillars)
    
    # move simulation
    while True:
        move_made = False

        # iterate through each dicted top colors of pillars (color: index)
        for color, indices in list(top_colors_of_pillars.items()):
            if len(indices) >= 2: # a move can be made from it (since there are more than 2 pillars that have matching top)
                move_made = True

                # if so, we pop the top block from both pillars
                for _ in range(2):
                    pillar = indices.pop() # pop the top in a dicted pillar
                    stacks[pillar].pop() # pop also the top in the actual stack

                    # update dicted for the reference of the next generations of moves
                    if stacks[pillar]:
                        new_top = stacks[pillar][-1] 
                        top_colors_of_pillars[new_top].append(pillar)

                print("INDICES", indices)
                print(top_colors_of_pillars)

                # in order for the loop not to loop forever in the top_colors_of_pillars, we have to delete
                if not indices:
                    del top_colors_of_pillars[color]
                break
        
        if not move_made:
            break
    
    print("STACKS NOW", stacks)

    return all(len(stack) == 0 for stack in stacks)

print(winnable(2, [[1, 2], [1, 2]]))
print(winnable(2, [[1, 2], [2, 1]]))
print(winnable(3, [[1, 2, 3], [1, 2], [3]]))
print(winnable(3, [[3, 2, 1], [1, 2], [3]]))
print(winnable(3, [[3], [1, 2, 3], [1, 2]]))
print(winnable(3, [[1, 2, 3], [3], [1, 2]]))
print(winnable(4, [[4], [3, 4], [1, 2, 3], [1, 2]]))
assert winnable(2, [[1, 2], [1, 2]]) is True
assert winnable(2, [[1, 2], [2, 1]]) is False
assert winnable(1, [[1, 1]]) is False
