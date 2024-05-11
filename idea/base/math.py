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
