from idea.base.data import Block
from idea.algorithm.round import round, final_round


class IDEA:
    def __init__(self, plain_text:bytes, key:bytes) -> None:
        if w := len(plain_text) % 8 != 0:
            zero_padding = bytearray(8 - w)
            plain_text += zero_padding
        self.plain_text = Block(plain_text)
        self.key = Block(key)
        self.sub_keys = self.generate_sub_keys(Block(key))

    def generate_sub_keys(self, key:Block) -> list[Block]:
        sub_keys = []
        while len(sub_keys) < 52:
            sub_keys.extend(list(key.break_into_sub_blocks(2)))
            key <<= 25
        return sub_keys[:52]

    def _encrypt_block(self, block_64:Block) -> Block:
        sub_block_16 = tuple(block_64.break_into_sub_blocks(2))
        for i in range(8):
            sub_block_16 = round(sub_block_16, self.sub_keys[i * 6:i * 6 + 6])
        return Block.join(final_round(sub_block_16, self.sub_keys[48:]))

    def encrypt(self) -> bytes:
        cipher_text = b''
        for block_64 in self.plain_text.break_into_sub_blocks(8):
            cipher_block = self._encrypt_block(block_64)
            cipher_text += cipher_block.data
        return cipher_text
    
    def CBC_encrypt(self) -> bytes:
        cipher_text = b''
        last_cipher_block = Block(b'\x00' * 8)
        for block_64 in self.plain_text.break_into_sub_blocks(8):
            block_64 = block_64 ^ last_cipher_block
            last_cipher_block = self._encrypt_block(block_64)
            cipher_text += last_cipher_block.data
        return cipher_text

    def CTR_encrypt(self) -> bytes:
        cipher_text = b''
        for counter, block_64 in enumerate(self.plain_text.break_into_sub_blocks(8)):
            cipher_counter = self._encrypt_block(counter.to_bytes(8))
            cipher_block = block_64 ^ cipher_counter
            cipher_text += cipher_block.data
        return cipher_text
