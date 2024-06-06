from hash.utils import Block, S_Box


class MyHash:
    def __init__(self, plain_text:bytes, keys:list[bytes], salt:bytes, work_factor:int, sbox:list[S_Box]) -> None:
        if len(salt) != 8:
            raise ValueError('Salt must be 8 bytes long')
        if len(plain_text) != 8:
            raise ValueError('Plain text must be 8 bytes long')
        if len(keys) != 32:
            raise ValueError('Keys must be 32')
        for key in keys:
            if len(key) != 4:
                raise ValueError('Each key must be 4 bytes long')
        if len(sbox) != 4:
            raise ValueError('S-Boxes must be 4')
        self.plain_text = Block(plain_text)
        self.keys = list(map(Block, keys))
        self.salt = Block(salt)
        self.work_factor = work_factor
        self.sbox = sbox

    def encrypt(self) -> bytes:
        cipher_text = self.plain_text
        for _ in range(2 ** self.work_factor):
            cipher_text = self.box(cipher_text, self.keys) ^ self.salt
        return cipher_text

    def box(self, input_64:Block, keys:list[Block]) -> Block:
        for i in range(32):
            input_64 = self.round(input_64, keys[i])
        input_64 = self.final_round(input_64, keys)
        return input_64

    def round(self, input_64:Block, key:Block) -> Block:
        left_32, right_32 = input_64[:4], input_64[4:]
        return Block.join(self.w(left_32 ^ key) ^ right_32, left_32)

    def final_round(self, input_64:Block, keys:list[Block]) -> Block:
        left_32, right_32 = input_64[:4], input_64[4:]
        return Block.join(right_32 ^ keys[31], left_32 ^ keys[30])

    def w(self, input_32:Block) -> Block:
        a = self.sbox[0].substitute(input_32[:1]) + self.sbox[1].substitute(input_32[1:2])
        b = self.sbox[2].substitute(input_32[2:3]) ^ a
        return self.sbox[3].substitute(input_32[3:]) + b
