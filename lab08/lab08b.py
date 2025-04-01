# type: ignore

from collections import defaultdict
from collections.abc import Sequence

Die = tuple[int, int, int, int, int, int]

def longest_sequence(dice: Sequence[Die]) -> int:
    # Build a dictionary: for each number, list the dice indices that have that face.
    avail = defaultdict(list)
    for i, die in enumerate(dice):
        # Using a set so that duplicates on one die don’t matter.
        for face in set(die):
            avail[face].append(i)
            
    if not avail:
        return 0

    # Sorted unique numbers that appear on some die.
    unique_nums = sorted(avail.keys())
    unique_set = set(unique_nums)
    
    # Precompute, for each candidate starting number (that is in avail),
    # how far does the consecutive block (of numbers that appear in avail) go?
    # (If from x every number x, x+1, ... x+block_len-1 is in unique_set.)
    block_end = {}  # x -> largest r (>=x) such that every integer from x to r is in unique_set.
    # We iterate in reverse order over unique_nums.
    last = -1
    for x in reversed(unique_nums):
        if last == -1 or last == x + 1:
            block_end[x] = x if last == -1 else block_end.get(x+1, x)
        else:
            block_end[x] = x
        last = x
    
    global_best = 0
    n_unique = len(unique_nums)
    
    # we'll use an incremental DFS–based matching for a given starting value L.
    # For the current candidate starting number L, we want to assign dice for numbers:
    # L, L+1, L+2, ... up to some limit. (We only try until the consecutive block from L ends.)
    def can_assign(num, used):
        # Try to assign a die for number 'num' (or reassign if necessary)
        for die in avail[num]:
            if used[die]:
                continue
            used[die] = True
            # If die is not used yet in matching, or if we can reassign its current number:
            if match[die] is None or can_assign(match[die], used):
                match[die] = num
                return True
        return False

    for L in unique_nums:
        r = block_end[L]
        possible = r - L + 1
        if possible <= global_best:
            continue

        match = [None] * len(dice)
        cur_chain = 0
        
        n = L
        while n in avail:
            used = [False] * len(dice)
            if can_assign(n, used):
                cur_chain += 1
                n += 1
            else:
                break
                
        if cur_chain > global_best:
            global_best = cur_chain
            if global_best == len(dice):
                break

    return global_best
    