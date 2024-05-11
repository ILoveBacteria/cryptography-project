from idea.base.math import add, multiple


class Block:
    def __init__(self, data:int):
        self.data = data
    
    def __add__(self, other):
        return Block(add(self.data, other.data))

    def __mul__(self, other):
        return Block(multiple(self.data, other.data))

    def __xor__(self, other):
        return Block(self.data ^ other.data)
