# type: ignore

import sys, math

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    
    # freq[x] will count numbers equal to x (only for x <= m)
    freq = [0] * (m+1)
    # pos[x] will store list of positions (1-indexed) where number x occurs.
    pos = [[] for _ in range(m+1)]
    
    arr = []
    for i in range(n):
        a = int(next(it))
        arr.append(a)
        if a <= m:
            freq[a] += 1
            pos[a].append(i+1)  # store 1-indexed positions

    # count[L] = number of numbers in the array (<= m) that divide L.
    count = [0] * (m+1)
    # For each possible number d that appears in our array (d in 1..m),
    # add its frequency to every multiple of d.
    for d in range(1, m+1):
        if freq[d] > 0:
            for multiple in range(d, m+1, d):
                count[multiple] += freq[d]
    
    # Choose the candidate L in 1..m with maximum count.
    best = 1
    for L in range(1, m+1):
        if count[L] > count[best]:
            best = L

    # If best candidate yields 0 numbers, then answer is the empty subsequence.
    if count[best] == 0:
        sys.stdout.write("1 0\n")
        return

    # Reconstruct the subsequence: we want all indices where a divides best.
    chosen_indices = []
    for d in range(1, m+1):
        if best % d == 0:
            # add all indices corresponding to number d
            chosen_indices.extend(pos[d])
    
    chosen_indices.sort()
    
    # Compute the LCM of the chosen numbers.
    current_lcm = 1
    for idx in chosen_indices:
        # Only consider numbers that are <= m (they all are by our collection)
        a_val = arr[idx-1]
        current_lcm = current_lcm * a_val // math.gcd(current_lcm, a_val)
    
    # Output: LCM and length, then positions.
    out_lines = []
    out_lines.append(f"{current_lcm} {len(chosen_indices)}")
    out_lines.append(" ".join(map(str, chosen_indices)))
    sys.stdout.write("\n".join(out_lines))
    
if __name__ == '__main__':
    main()
