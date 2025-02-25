# type: ignore

from collections import defaultdict
from itertools import product

def longest_game(l: int, alphabet: str) -> str:
    nodes = [''.join(p) for p in product(alphabet, repeat=l-1)]

    graph = defaultdict(list)
    for node in nodes:
        for char in alphabet:
            new_word = node + char 
            next_node = new_word[-(l-1):]  
            graph[node].append(next_node)


    start_node = nodes[0]

    for i in graph.keys():
        print(i, graph[i])

    def hierholzer(start):
        path = []
        stack = [start]
        while stack:
            u = stack[-1]
            if graph[u]:
                v = graph[u].pop()
                stack.append(v)
            else:
                path.append(stack.pop())
        return path[::-1]  

    eulerian_path = hierholzer(start_node)

    print("euler_path", eulerian_path)

    result = eulerian_path[0]
    for i in range(1, len(eulerian_path)):
        # print(eulerian_path[i][-1])
        result += eulerian_path[i][-1]  

    return result

print(longest_game(2, "ei"))  # Expected: "eiiee"
print(longest_game(3, "abc"))  # Should return a valid sequence
print(longest_game(3, "01"))  # Should return a de Bruijn sequence for binary digits
print(longest_game(4, "ab"))  # Testing longer sequences