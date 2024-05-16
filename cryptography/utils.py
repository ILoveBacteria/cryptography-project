from typing import Generator, Iterable


class Block:
    @classmethod
    def join(cls, blocks:Iterable['Block']) -> 'Block':
        return Block(b''.join(block.data for block in blocks))
    
    def break_into_sub_blocks(self, size:int) -> Generator['Block']:
        if size < 1:
            raise ValueError('Size must be greater than 0!')
        if size > len(self):
            raise ValueError('Size must be less than the length of the block!')
        if len(self) % size != 0:
            raise ValueError('Size must be a divisor of the length of the block!')
        for i in range(0, len(self), size):
            yield Block(self.data[i:i + size])

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
    
    def __lshift__(self, other):
        return Block(circular_left_shift(self.data, other))
    

def add(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    addition_modulo = 2 ** (len(d1) * 8)
    return ((int.from_bytes(d1) + int.from_bytes(d2)) % addition_modulo).to_bytes(len(d1))


def multiple(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    multiple_modulo = 2 ** (len(d1) * 8) + 1
    return ((int.from_bytes(d1) + int.from_bytes(d2)) % multiple_modulo).to_bytes(len(d1))


def xor(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    return (int.from_bytes(d1) ^ int.from_bytes(d2)).to_bytes(len(d1))


def circular_left_shift(d:bytes, n:int) -> bytes:
    d_int = int.from_bytes(d)
    return ((d_int << n) | (d_int >> (len(d) - n))).to_bytes(len(d))
