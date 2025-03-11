# type: ignore

from collections import Counter

from utils import Edge, CS33Random

from hierholzer import find_eulerian_path

def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7

    for cas in range(T):

        n = rand.randint(1, rand.choice([3, 11, 31, 111]))
        e = rand.randint(0, rand.choice([3, 11, 31, 111])) + n - 1 if n > 0 else 0
        edges = rand.random_connected_graph(n, e)
        assert len(edges) == e



        eulpath = find_eulerian_path(n, edges)
        
        print(f"Trying case {cas} of {T}: {n=} {e=}")


        odd_degs = sum(deg % 2 for deg in Counter(node for edge in edges for node in (edge.i, edge.j)).values())
        assert odd_degs % 2 == 0

        assert (eulpath is not None) == (odd_degs <= 2)

        # check
        if eulpath is not None:
            assert len(eulpath) == e + 1
            cedges = []
            s = eulpath[0].j
            assert eulpath[0].edge is None
            for ea in eulpath[1:]:
                i, j = ea.edge.i, ea.edge.j
                if i != s: i, j = j, i
                assert i == s
                cedges.append(ea.edge)
                s = j

            assert sorted(edges) == sorted(cedges)




if __name__ == '__main__':
    main()
