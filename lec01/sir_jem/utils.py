# type: ignore

from dataclasses import dataclass

@dataclass
class Edge:
    i: int
    j: int
    cost: int


# TODO subclass random.Random in the future
def shuffled(rand, seq):
    seq = [*seq]
    rand.shuffle(seq)
    return seq


def make_adjacency_list(nodes, edges):
    adj = {node: [] for node in nodes}

    for edge in edges:
        adj[edge.i].append((edge.j, edge.cost))
        adj[edge.j].append((edge.i, edge.cost))

    return adj
