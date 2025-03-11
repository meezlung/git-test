# type: ignore

from utils import Edge, CS33Random
from persistent_stack_brute import Stack as StackBrute
from persistent_stack import Stack as Stack


stack_classes = (
    StackBrute,
    Stack,
)


def simulate_persistent_stack_ops(Stack, ops):
    return list(_simulate_persistent_stack_ops(Stack, ops))


def _simulate_persistent_stack_ops(Stack, ops):
    stack_histories = []
    for typ, *data in ops:
        match typ:
            case 'make':
                # make a new stack history
                stack_histories.append([Stack()])
            case 'push':
                idx, val = data
                assert 0 <= idx < len(stack_histories)
                stack_history = stack_histories[idx]
                s = stack_history[-1]
                t = s.push(val)
                stack_history.append(t)
            case 'pop':
                idx, = data
                assert 0 <= idx < len(stack_histories)
                stack_history = stack_histories[idx]
                s = stack_history[-1]
                try:
                    v, t = s.pop()
                except ValueError:
                    t = s
                    yield None
                else:
                    yield v
                stack_history.append(t)
            case 'len':
                idx, = data
                assert 0 <= idx < len(stack_histories)
                stack_history = stack_histories[idx]
                s = stack_history[-1]
                yield len(s)
            case 'revert':
                # revert to version vidx
                idx, vidx = data
                assert 0 <= idx < len(stack_histories)
                stack_history = stack_histories[idx]
                assert 0 <= vidx < len(stack_history)
                t = stack_history[vidx]
                stack_history.append(t)
            case _:
                raise ValueError


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7
    for cas in range(T):
        ops = rand.random_persistent_stack_ops()

        # print(ops)
        print(f"Trying case {cas} of {T}: q={len(ops)}")

        answers = [simulate_persistent_stack_ops(stack_class, ops) for stack_class in stack_classes]

        # print(answers)

        assert all(answer == answers[0] for answer in answers)


if __name__ == '__main__':
    main()
