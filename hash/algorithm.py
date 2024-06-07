from hash.utils import Block, S_Box


class MyHash:
    def __init__(self, keys:list[int], sbox:list[S_Box]) -> None:
        if len(keys) != 32:
            raise ValueError('Keys must be 32')
        if len(sbox) != 4:
            raise ValueError('S-Boxes must be 4')
        keys = list(map(lambda x: x.to_bytes(4, 'big'), keys))
        self.keys = list(map(Block, keys))
        self.sbox = sbox

    def encrypt(self, plain_text:int, salt:int, work_factor:int) -> Block:
        plain_text = Block(plain_text.to_bytes(8, 'big'))
        salt = Block(salt.to_bytes(8, 'big'))
        cipher_text = plain_text
        for _ in range(2 ** work_factor):
            cipher_text = self.box(cipher_text, self.keys) ^ salt
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
