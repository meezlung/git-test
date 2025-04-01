# type: ignore

from collections.abc import Sequence
from collections import defaultdict

Die = tuple[int, int, int, int, int, int]

def bipartite_matching(n, m, edges):
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
    
    to_left = [-1] * m  # right node to left node
    to_right = [-1] * n  # left node to right node

    def augment(u, visited):
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                if to_left[v] == -1 or augment(to_left[v], visited):
                    to_left[v] = u
                    to_right[u] = v
                    return True
        return False

    match_count = 0
    for u in range(n):
        visited = [False] * m
        if augment(u, visited):
            match_count += 1

    return match_count, to_left, to_right

def choose_faces(dice: Sequence[Die]) -> list[int]:
    d = len(dice)
    if d == 0:
        return []
    
    processed_dice = []
    num_to_faces_list = []
    for die in dice:
        faces = [(num, idx + 1) for idx, num in enumerate(die)]
        faces.sort()
        num_map = defaultdict(list)
        for num, idx in faces:
            num_map[num].append(idx)
        processed_dice.append(faces)
        num_to_faces_list.append(num_map)

    all_numbers = set()
    for die in dice:
        all_numbers.update(die) # lagay lahat ng klaseng "kinds" of numbers sa all numbers for max finding

    max_num = max(all_numbers) if all_numbers else 0 # find max
    
    presence = [0] * (max_num + 2) # this is to check which numbers are present in any die (+2 para safe for dp)

    for num in all_numbers:
        presence[num] = 1
    
    prefix = [0] * (max_num + 2) # prefix for O(1) range sum checks
    for i in range(1, max_num + 2):
        prefix[i] = prefix[i-1] + presence[i-1]

    max_x = max(14000 - d + 1, 0) # max number possible is 14000 (constraints), this designed to determine the maximum possible starting value of x for a consecutive sequence of length d such that di sya sosobra sa 14000
    
    for x in range(1, max_x + 1):
        # x is the possible candidate for starting number of the consecutive seq
        # x_end is the possible candidate for ending number of the consecutive seq 
        x_end = x + d - 1

        if x_end > max_num:
            continue
        if (prefix[x_end + 1] - prefix[x]) != d:
            continue
        
        valid = True
        for die_faces in processed_dice:
            # binary search to find the smallest first number >= x in the die
            left, right = 0, 5
            pos = 6
            while left <= right:
                mid = (left + right) // 2
                if die_faces[mid][0] >= x:
                    pos = mid
                    right = mid - 1
                else:
                    left = mid + 1

            # ensure every die has at least one number in the range [x, x_end], if not invalid
            if pos >= 6 or die_faces[pos][0] > x_end:
                valid = False
                break

        if not valid:
            continue # end agad if invalid so no overthink
        
        # build bipartite
        numbers = list(range(x, x_end + 1)) # the candidates
        num_to_idx = {num: i for i, num in enumerate(numbers)}
        adj = [[] for _ in range(d)]
        edges = []
        for i in range(d):
            die_map = num_to_faces_list[i]
            for num in numbers:
                if num in die_map: # if the candidate is in a die
                    adj[i].append(num_to_idx[num])


            for j in adj[i]:
                edges.append((i, j))

        match_count, to_left, to_right = bipartite_matching(d, d, edges)
        if match_count == d: # this should be true
            answer = []
            for i in range(d):
                num_idx = to_right[i]
                num = numbers[num_idx]
                answer.append(num_to_faces_list[i][num][0])
            return answer
    
    return [1] * d # wala naman na to siguro since guaranteed na valid lahat
