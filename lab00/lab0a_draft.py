# n pet slimes, where the size of ith slime is s[i]

# after one day,
#  If the size of the slime is a two-digit integer "XY", it splits into two slimes with sizes X and Y.
#     If Y is 0, the second slime immediately disappears after the split (aw).
#  Otherwise, it doubles in size.

# After d days, how many pet slimes will you have?

# The answer can be very large, so only output it mod 1,000,000,000

def num_slimes_after(sizes: list[int], d: int) -> int:
    sizes_copy = sizes.copy()

    for _ in range(d):
        new_sizes: list[int] = []
        
        # iterate through each size
        for size in sizes_copy:
            if 10 <= size < 100: # if two digit number
                x = size // 10
                y = size % 10
                new_sizes.append(x)
                if y != 0: # if y is not 0
                    new_sizes.append(y)

            else:
                new_sizes.append(size * 2)
        sizes_copy = new_sizes


    return len(sizes_copy)%1_000_000_000