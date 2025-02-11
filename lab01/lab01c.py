from collections.abc import Sequence
from collections import deque

Pair = tuple[str, str]

def bfs(start: str, end: str, adj_list: dict[str, list[str]]) -> bool:
    if start == end:
        return True
    
    queue = deque([start])
    visited = set([start])

    while queue:
        node = queue.popleft()
        if node in adj_list:
            for neighbor in adj_list[node]:
                if neighbor == end:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    return False

def is_supereffective(info: Sequence[Pair], questions: Sequence[Pair]) -> list[bool]:
    # adj list 
    adj_list: dict[str, list[str]] = {}

    for i, j in info:
        if i not in adj_list:
            adj_list[i] = []
        adj_list[i].append(j)

    answers: list[bool] = []

    # implement prim-like alg
    for c, d in questions:
        answers.append(bfs(c, d, adj_list))

    return answers