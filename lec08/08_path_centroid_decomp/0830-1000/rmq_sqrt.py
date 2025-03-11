# type: ignore

from collections.abc import Sequence
from math import sqrt, inf


class RMQ:
    def __init__(self, values: Sequence[int]):
        self.values = list(values)

        self.b = 1 + int(round(sqrt(len(values))))

        self.block_mins = [inf]*(len(values) // self.b + 2)

        for bi in range(len(self.block_mins)):
            self.update_block(bi)

        super().__init__()


    def __len__(self) -> int:
        return len(self.values)


    def range_min(self, i: int, j: int):
        assert 0 <= i <= j <= len(self)
        ans = inf

        # left butal
        while i < j and i % self.b != 0:
            ans = min(ans, self.values[i])
            i += 1

        # right butal
        while i < j and j % self.b != 0:
            j -= 1
            ans = min(ans, self.values[j])

        if i < j:
            # full blocks
            assert i % self.b == j % self.b == 0
            i //= self.b
            j //= self.b
            while i < j:
                ans = min(ans, self.block_mins[i])
                i += 1

        return ans


    def __setitem__(self, i: int, v: int) -> None:
        assert 0 <= i < len(self)
        self.values[i] = v

        # update block as well
        self.update_block(i // self.b)


    def update_block(self, bi: int) -> None:
        assert 0 <= bi < len(self.block_mins)
        self.block_mins[bi] = inf
        for i in range(bi * self.b, min((bi + 1) * self.b, len(self))):
            self.block_mins[bi] = min(self.block_mins[bi], self.values[i])
