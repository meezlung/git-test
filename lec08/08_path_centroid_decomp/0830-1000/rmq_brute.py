# type: ignore

from collections.abc import Sequence
from math import inf


class RMQ:
    def __init__(self, values: Sequence[int]):
        self.values = list(values)
        super().__init__()


    def __len__(self) -> int:
        return len(self.values)


    def range_min(self, i: int, j: int):
        assert 0 <= i <= j <= len(self)
        return min(self.values[i:j], default=inf)


    def __setitem__(self, i: int, v: int) -> None:
        assert 0 <= i < len(self)
        self.values[i] = v
