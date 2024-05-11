ADDITION_MODULO = 2**16
MULTIPLE_MODULO = 2**16 + 1

def add(d1:int, d2:int) -> int:
    return (d1 + d2) % ADDITION_MODULO


def multiple(d1:int, d2:int) -> int:
    return (d1 * d2) % MULTIPLE_MODULO
