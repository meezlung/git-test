# n pet slimes, where the size of ith slime is s[i]

# after one day,
#  If the size of the slime is a two-digit integer "XY", it splits into two slimes with sizes X and Y.
#     If Y is 0, the second slime immediately disappears after the split (aw).
#  Otherwise, it doubles in size.

# After d days, how many pet slimes will you have?

# The answer can be very large, so only output it mod 1,000,000,000

from collections import defaultdict

def num_slimes_after(sizes: list[int], d: int) -> int:

    slime_count: defaultdict[int, int] = defaultdict(int)
    for size in sizes:
        slime_count[size] += 1

    for _ in range(d):
        new_slime_count: defaultdict[int, int] = defaultdict(int)
        print(slime_count)

        for size, count in slime_count.items():
            if 10 <= size < 100:  # if two-digit number
                x = size // 10 
                y = size % 10
                new_slime_count[x] += count
                if y != 0:  # if y is not 0
                    new_slime_count[y] += count
            else:
                new_slime_count[size * 2] += count

        print(new_slime_count)

        slime_count = new_slime_count

    print()
    return sum(slime_count.values()) % 1_000_000_000

assert num_slimes_after([3, 6], 2) == 3
