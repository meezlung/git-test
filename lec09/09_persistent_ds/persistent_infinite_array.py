# type: ignore

class InfArray:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left or self
        self.right = right or self
        super().__init__()

    def __getitem__(self, i):
        if i == 0:
            return self.value
        elif i % 2 != 0:
            return self.left[(i - 1) // 2]
        else:
            assert i % 2 == 0
            return self.right[(i - 1) // 2]

    def assign(self, i, v):
        if i == 0:
            return InfArray(value=v, left=self.left, right=self.right)
        elif i % 2 != 0:
            return InfArray(value=self.value, left=self.left.assign((i - 1) // 2, v), right=self.right)
        else:
            assert i % 2 == 0
            return InfArray(value=self.value, left=self.left, right=self.right.assign((i - 1) // 2, v))
