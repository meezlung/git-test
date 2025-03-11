# type: ignore

from dataclasses import dataclass


# very slow set that just copies the contents every time there's a modification
class Set:
    def __init__(self, contents=()):
        self.contents = set(contents)
        super().__init__()


    def add(self, val):
        return Set(self.contents | {val})


    def __contains__(self, val):
        return val in self.contents
