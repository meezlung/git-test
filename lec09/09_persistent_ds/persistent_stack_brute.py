# type: ignore

from collections.abc import Iterable


# very slow stack that just copies the contents every time there's a modification
class Stack[T]:
    def __init__(self, contents: Iterable[T] = ()):
        self.contents = list(contents)
        super().__init__()

    def push(self, value) -> "Stack[T]":
        return Stack([*self.contents, value])

    def pop(self) -> "tuple[T, Stack[T]]":
        if not self.contents:
            raise ValueError
        *rest, top = self.contents
        return top, Stack(rest)

    def __len__(self):
        return len(self.contents)
