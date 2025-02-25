# in minecraft, you're currently looking for diamonds, and you want to stock up on a bunch of supplies:
# torches: 1 stick, 1 coal. crafting 1 torch gives t experience
# ladders: 7 sticks. crafting 1 ladder gives l experience
# cooked meat: cooking each piece of cooked meat in the furnace uses up 3 coal. each piece cooked gives m experience.

# you currently have s sticks and c coal
# If you carefully decide how much of each item you make, what is the maximum amount of experience you can gain?

#   Note that:

#     You are not required to use up all sticks and coal.
#     You may make 0 of some item.

# type: ignore

# def most_xp(s: int, c: int, t: int, l: int, m: int) -> int:
#     max_xp = 0

#     # try all possible combinations of torches, ladders, and cooked meat
#     for torches in range(min(s, c) + 1):
#         for ladders in range((s - torches) // 7 + 1):
#             rem_coal = c - torches
#             cooked_meat = rem_coal // 3
#             xp = torches * t + ladders * l + cooked_meat * m
#             max_xp = max(max_xp, xp)

#     return max_xp

def most_xp(s: int, c: int, t: int, l: int, m: int) -> int:
    max_xp = 0

    max_torches = min(s, c)

    for torches in range(max_torches + 1):
        rem_sticks = s - torches
        rem_coal = c - torches

        # calculate max ladders we can make
        ladders = rem_sticks // 7

        # calculate max cooked meat we can make
        cooked_meat = rem_coal // 3

        # calculate total XP
        xp = torches*t + ladders*l + cooked_meat*m
        max_xp = max(max_xp, xp)

    return max_xp

assert most_xp(14, 9, 1, 10, 20) == 80
