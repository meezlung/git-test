# type: ignore

from utils import Edge, CS33Random


from lca_brute0 import RootedTree as RootedTreeBrute0
from lca_brute1 import RootedTree as RootedTreeBrute1
from lca_brute2 import RootedTree as RootedTreeBrute2
from lca_brute3 import RootedTree as RootedTreeBrute3
from lca_fast import RootedTree as RootedTreeFast


RootedTreeClasses = (
    RootedTreeBrute0,
    RootedTreeBrute1,
    RootedTreeBrute2,
    RootedTreeBrute3,
    RootedTreeFast,
)


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7

    for cas in range(T):

        n = rand.randint(1, rand.choice([3, 11, 31, 111]))
        q = rand.randint(1, rand.choice([3, 11, 31, 111]))

        # make random rooted tree
        nodes = rand.shuffled(range(n))
        parent = [*range(n)]
        for i in range(1, n):
            j = rand.randrange(i)
            parent[nodes[i]] = nodes[j]
        root = nodes[0]
        parent[root] = root

        print(f"Trying case {cas} of {T}: {n=} {parent=}")

        # initialize trees
        trees = [RootedTree(parent, root) for RootedTree in RootedTreeClasses]

        # answer random queries
        for _ in range(q):
            i, j = rand.choices(range(n), k=2)

            answers = [tree.lca(i, j) for tree in trees]

            assert all(answer == answers[0] for answer in answers)


if __name__ == '__main__':
    main()
