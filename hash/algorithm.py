from cryptography.utils import Block


class MyHash:
    def __init__(self, plain_text:bytes, keys:list[bytes], salt:bytes, work_factor:int) -> None:
        if len(salt) != 8:
            raise ValueError('Salt must be 8 bytes long')
        if len(plain_text) != 8:
            raise ValueError('Plain text must be 8 bytes long')
        if len(keys) != 32:
            raise ValueError('Keys must be 32')
        for key in keys:
            if len(key) != 4:
                raise ValueError('Each key must be 4 bytes long')
        self.plain_text = Block(plain_text)
        self.keys = list(map(Block, keys))
        self.salt = Block(salt)
        self.work_factor = work_factor

    def encrypt(self) -> bytes:
        cipher_text = self.plain_text
        for _ in range(2 ** self.work_factor):
            cipher_text = self.box(cipher_text, self.key) ^ self.salt
        return cipher_text
    
    def box(self) -> Block:
        cipher_text = self.plain_text
        for i in range(32):
            cipher_text = self.round(cipher_text, self.keys[i])
        cipher_text = self.final_round(cipher_text, self.keys[i])
        return cipher_text

    def round(self, input:Block, key:Block) -> Block:
        left, right = input[:4], input[4:]
        return Block.join(w(left ^ key) ^ right, left)

    def final_round(self, input:Block) -> Block:
        left, right = input[:4], input[4:]
        return Block.join(right ^ self.keys[31], left ^ self.keys[30])


def w():
    pass



