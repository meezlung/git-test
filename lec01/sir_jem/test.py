# type: ignore

from random import Random

from utils import Edge, shuffled

from kruskal import mst_cost as mst_cost_kruskal
from prim import mst_cost as mst_cost_prim
from prim2 import mst_cost as mst_cost_prim2
from boruvka import mst_cost as mst_cost_boruvka


def main():
    rand = Random(33)

    def random_tree(nodes):
        nodes = shuffled(rand, nodes)
        for i in range(1, len(nodes)):
            j = rand.randrange(i)
            i, j = shuffled(rand, (i, j))
            yield Edge(nodes[i], nodes[j], rand_cost())

    def rand_cost():
        return rand.randint(1, rand.choice([3, 11, 31, 111]))

    def random_connected_graph():
        n = rand.randint(1, rand.choice([3, 11, 21, 31]))
        e = rand.randint(0, rand.choice([3, 11, 21, 31]))
        nodes = range(n)

        def rand_edge():
            i, j = rand.choices(nodes, k=2)
            return Edge(i, j, rand_cost())

        edges = [rand_edge() for _ in range(e)]

        # add a random tree
        edges += random_tree(nodes)

        return nodes, shuffled(rand, edges)

    # ten million tests
    T = 10**7
    for cas in range(T):
        nodes, edges = random_connected_graph()

        # print()
        print(f"Trying case {cas} of {T}")
        # print('    nodes:', *nodes)
        # for edge in edges:
        #     print('    edge:', edge)

        cost_kruskal = mst_cost_kruskal(nodes, edges)
        cost_prim = mst_cost_prim(nodes, edges)
        cost_prim2 = mst_cost_prim2(nodes, edges)
        cost_boruvka = mst_cost_boruvka(nodes, edges)

        print("The mst cost is", cost_kruskal, cost_prim, cost_prim2, cost_boruvka)

        assert cost_kruskal == cost_prim == cost_prim2 == cost_boruvka


if __name__ == '__main__':
    main()
