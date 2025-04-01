# type: ignore
class OrderedSet:
    def __init__(self):
        self.contents = []
        super().__init__()


    def add(self, val):
        self.contents.append(val)


    def remove(self, val):
        self.contents = [v for v in self.contents if v != val]


    def __contains__(self, val):
        return val in self.contents
