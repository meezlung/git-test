# type: ignore
from utils import Edge, CS33Random


from bridges_and_articulation_points_brute import bridges_and_articulation_points as cut_brute
from bridges_and_articulation_points_dfs import bridges_and_articulation_points as cut_dfs
from sccs_brute import sccs as sccs_brute
from sccs_kosaraju import sccs as sccs_kosaraju

cut_sols = (
    cut_brute,
    cut_dfs,
)

sccs_sols = (
    sccs_brute,
    sccs_kosaraju,
)

def normalize_cut(cut_nodes, cut_edges):
    return sorted(cut_nodes), sorted(cut_edges)


def normalize_sccs(sccs):
    return sorted(map(sorted, sccs))


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7

    for cas in range(T):

        def test_cut():
            # test bridges and articulation points (connected graphs)
            n = rand.randint(0, rand.choice([3, 11, 31, 111]))
            e = rand.randint(0, rand.choice([3, 11, 31, 111])) + n - 1 if n > 0 else 0
            edges = rand.random_connected_graph(n, e)
            assert len(edges) == e


            print(f"Trying case {cas} of {T}: {n=} {e=}")

            # cut sols
            answers = [normalize_cut(*cut(n, edges)) for cut in cut_sols]

            # print(n, e)
            # for edge in edges: print(f'    {edge.i} -- {edge.j}')
            # for ans in answers:
            #     print(ans)

            assert all(answer == answers[0] for answer in answers)


        def test_sccs():
            # test SCCs

            n = rand.randint(0, rand.choice([3, 11, 31, 111]))
            e = rand.randint(0, rand.choice([3, 11, 31, 111])) if n > 0 else 0
            edges = rand.random_graph(n, e)
            assert len(edges) == e


            print(f"Trying case {cas} of {T}: {n=} {e=}")

            # cut sols
            answers = [normalize_sccs(sccs(n, edges)) for sccs in sccs_sols]

            # print(n, e)
            # for edge in edges: print(f'    {edge.i} -> {edge.j}')
            # for ans in answers:
            #     print(ans)

            assert all(answer == answers[0] for answer in answers)


        test_cut()
        test_sccs()


if __name__ == '__main__':
    main()
