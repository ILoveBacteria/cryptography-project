import re

from hash.algorithm import MyHash
from hash.utils import S_Box, Block


def main():
    plain_text = b'12345678'
    keys = [
        0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344,
        0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89,
        0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
        0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917,
        0x9216D5D9, 0x8979FB1B, 0x38D01377, 0xA4093822,
        0xEC4E6C89, 0x243F6A88, 0x13198A2E, 0x85A308D3,
        0x082EFA98, 0x85A308D3, 0xBE5466CF, 0x03707344,
        0x243F6A88, 0x452821E6, 0x85A308D3, 0x38D01377,
    ]
    keys = list(map(lambda x: x.to_bytes(4, 'big'), keys))

    sbox_list = re.split(r'S-box \d\s+', open('sbox.txt').read().strip())[1:]
    sbox_list = list(map(lambda x: list(map(lambda y: list(map(lambda z: Block(int(z, 16).to_bytes(4, 'big')), y.strip().split())), x.strip().split('\n'))), sbox_list))
    sbox_list = list(map(S_Box, sbox_list))
    
    my_hash = MyHash(plain_text=plain_text,
                     keys=keys,
                     salt=b'12345678',
                     work_factor=1,
                     sbox=sbox_list)
    print(my_hash.encrypt())


if __name__ == '__main__':
    main()
