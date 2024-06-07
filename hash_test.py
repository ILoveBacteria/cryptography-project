import re

from hash.algorithm import MyHash
from hash.utils import S_Box, Block


def main():
    keys = re.split(r',\s+', open('keys.txt').read().strip())
    keys = list(map(lambda x: int(x, 16), keys))

    sbox_list = re.split(r'S-box \d\s+', open('sbox.txt').read().strip())[1:]
    sbox_list = list(map(lambda x: list(map(lambda y: list(map(lambda z: Block(int(z, 16).to_bytes(4, 'big')), y.strip().split())), x.strip().split('\n'))), sbox_list))
    sbox_list = list(map(S_Box, sbox_list))
    
    my_hash = MyHash(keys=keys, sbox=sbox_list)
    print(my_hash.encrypt(plain_text=0x0, 
                          salt=0x701309b2b76e6e2d, 
                          work_factor=1))


if __name__ == '__main__':
    main()
