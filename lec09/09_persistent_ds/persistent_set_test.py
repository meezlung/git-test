# type: ignore
from utils import Edge, CS33Random
from persistent_set_brute import Set as SetBrute
from persistent_set import Set as Set


set_classes = (
    SetBrute,
    Set,
)


def simulate_persistent_set_ops(Set, ops):
    return list(_simulate_persistent_set_ops(Set, ops))


def _simulate_persistent_set_ops(Set, ops):
    set_histories = []
    for typ, *data in ops:
        match typ:
            case 'make':
                # make a new set history
                set_histories.append([Set()])
            case 'add':
                idx, val = data
                assert 0 <= idx < len(set_histories)
                set_history = set_histories[idx]
                s = set_history[-1]
                t = s.add(val)
                set_history.append(t)
            case 'contains':
                idx, val = data
                assert 0 <= idx < len(set_histories)
                set_history = set_histories[idx]
                s = set_history[-1]
                yield val in s
            case 'revert':
                # revert to version vidx
                idx, vidx = data
                assert 0 <= idx < len(set_histories)
                set_history = set_histories[idx]
                assert 0 <= vidx < len(set_history)
                t = set_history[vidx]
                set_history.append(t)


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7
    for cas in range(T):
        ops = rand.random_persistent_set_ops()

        # print(ops)
        print(f"Trying case {cas} of {T}: q={len(ops)}")

        answers = [simulate_persistent_set_ops(set_class, ops) for set_class in set_classes]

        # print(answers)

        assert all(answer == answers[0] for answer in answers)


if __name__ == '__main__':
    main()
