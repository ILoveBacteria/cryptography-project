from typing import Generator, Iterable


class S_Box:
    def __init__(self, matrix:list[list['Block']]):
        self.matrix = matrix

    def substitute(self, data:'Block') -> 'Block':
        if len(data) != 1:
            raise ValueError('Input data to S-Box should be 1 byte')
        column = int((Block(b'\x03') & data) | ((Block(b'\x80') & data) >> 5))
        row = int((Block(b'\x7F') & data) >> 2)
        return self.matrix[row][column]
        

class Block:
    @classmethod
    def join(cls, *args) -> 'Block':
        return Block(b''.join(block.data for block in args))

    def __init__(self, data:bytes):
        self.data = data
    
    def __add__(self, other):
        return Block(add(self.data, other.data))

    def __xor__(self, other):
        return Block(xor(self.data, other.data))
    
    def __and__(self, other):
        return Block(and_bit(self.data, other.data))
    
    def __or__(self, other):
        return Block(or_bit(self.data, other.data))
    
    def __int__(self):
        return int.from_bytes(self.data, 'big')
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return Block(self.data[key])
    
    def __rshift__(self, other):
        return Block(right_shift(self.data, other))
    
    def __repr__(self) -> str:
        return hex(int.from_bytes(self.data, 'big'))
    

def add(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    addition_modulo = 2 ** 32
    return ((int.from_bytes(d1, 'big') + int.from_bytes(d2, 'big')) % addition_modulo).to_bytes(len(d1), 'big')


def xor(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    return (int.from_bytes(d1, 'big') ^ int.from_bytes(d2, 'big')).to_bytes(len(d1), 'big')


def and_bit(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    return (int.from_bytes(d1, 'big') & int.from_bytes(d2, 'big')).to_bytes(len(d1), 'big')


def or_bit(d1:bytes, d2:bytes) -> bytes:
    if len(d1) != len(d2):
        raise ValueError('Two data must be the same size!')
    return (int.from_bytes(d1, 'big') | int.from_bytes(d2, 'big')).to_bytes(len(d1), 'big')


def right_shift(d:bytes, n:int) -> bytes:
    d_int = int.from_bytes(d, 'big')
    return (d_int >> n).to_bytes(len(d), 'big')
