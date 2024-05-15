from idea.base.math import add, multiple, xor


class Block:
    def __init__(self, data:bytes):
        self.data = data
    
    def __add__(self, other):
        return Block(add(self.data, other.data))

    def __mul__(self, other):
        return Block(multiple(self.data, other.data))

    def __xor__(self, other):
        return Block(xor(self.data, other.data))
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return Block(self.data[key])
