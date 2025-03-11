# type: ignore

from utils import Edge, CS33Random

from shortest_path1 import shortest_paths as sp1
from shortest_path2 import shortest_paths as sp2
from shortest_path3 import shortest_paths as sp3
from shortest_path4 import shortest_paths as sp4
from shortest_path5 import shortest_paths as sp5
from shortest_path_neg import shortest_paths as sp_neg

sols = sp1, sp2, sp3, sp4, sp5, sp_neg


def main():
    rand = CS33Random(33)

    def random_tree(nodes):
        nodes = rand.shuffled(nodes)
        for i in range(1, len(nodes)):
            j = rand.randrange(i)
            i, j = rand.shuffled((i, j))
            yield Edge(nodes[i], nodes[j], rand_cost())

    def rand_cost():
        # positive costs
        return rand.randint(1, rand.choice([3, 11, 31, 111]))

    def random_graph():
        n = rand.randint(1, rand.choice([3, 11, 21, 31]))
        e = rand.randint(0, rand.choice([3, 11, 21, 31]))
        nodes = range(n)

        def rand_edge():
            i, j = rand.choices(nodes, k=2)
            return Edge(i, j, rand_cost())

        edges = [rand_edge() for _ in range(e)]

        return n, edges


    def random_connected_graph():
        n, edges = random_graph()

        # add a random tree
        edges += random_tree(nodes)

        return n, shuffled(rand, edges)


    # ten million tests
    T = 10**7
    for cas in range(T):
        n, edges = random_graph()

        # print()
        print(f"Trying case {cas} of {T}: {n=} e={len(edges)}")
        # for edge in edges:
        #     print('    edge:', edge)

        answers = [sp(n, edges) for sp in sols]

        assert all(answer == answers[0] for answer in answers)

if __name__ == '__main__':
    main()
