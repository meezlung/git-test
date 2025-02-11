# type: ignore
from utils import Edge, CS33Random

from list import OrderedSet as ListSet
# from bst import OrderedSet as BSTSet
from treap import OrderedSet as TreapSet
# from avl import OrderedSet as AVLSet



set_classes = ListSet, TreapSet


def simulate_set_ops(Set, ops):
    return list(_simulate_set_ops(Set, ops))

def _simulate_set_ops(Set, ops):
    sets = []
    for typ, *data in ops:
        match typ:
            case 'make':
                sets.append(Set())
            case 'add':
                idx, val = data
                assert 0 <= idx < len(sets)
                sets[idx].add(val)
            case 'remove':
                idx, val = data
                assert 0 <= idx < len(sets)
                sets[idx].remove(val)
            case 'contains':
                idx, val = data
                assert 0 <= idx < len(sets)
                yield val in sets[idx]

def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7
    for cas in range(T):

        ops = rand.random_set_ops()


        # print(ops)
        print(f"Trying case {cas} of {T}: q={len(ops)}")

        answers = [simulate_set_ops(set_class, ops) for set_class in set_classes]

        # print(answers)

        assert all(answer == answers[0] for answer in answers)

if __name__ == '__main__':
    main()
