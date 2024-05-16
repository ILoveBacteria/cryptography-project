from typing import Generator

from idea.base.data import Block
from idea.algorithm.round import round, final_round


class IDEA:
    def __init__(self, plain_text:bytes, key:bytes) -> None:
        if w := len(plain_text) % 8 != 0:
            zero_padding = bytearray(8 - w)
            plain_text += zero_padding
        self.plain_text = Block(plain_text)
        self.key = Block(key)

    def generate_blocks_64bits(self) -> Generator[Block, None, None]:
        for i in range(0, len(self.plain_text), 8):
            yield Block(self.plain_text[i:i + 8])

    def generate_sub_keys(self, pre_shift:int) -> tuple[Block]:
        shifted_key = int.from_bytes(self.key) << pre_shift
        return (Block((shifted_key << i).to_bytes(2)) for i in range(6))

    def encrypt(self) -> bytes:
        cipher_text = b''
        for block_64 in self.generate_blocks_64bits():
            sub_block_16 = block_64.break_into_sub_blocks(2)
            for i in range(8):
                sub_block_16 = round(sub_block_16, self.generate_sub_keys(i * 6))
            cipher_block = Block.join(final_round(sub_block_16, self.generate_sub_keys(8 * 6)))
            cipher_text += cipher_block.data
        return cipher_text
    
    def CBC_encrypt(self) -> bytes:
        cipher_text = b''
        last_cipher_block = Block(b'\x00' * 8)
        for block_64 in self.generate_blocks_64bits():
            block_64 = block_64 ^ last_cipher_block
            sub_block_16 = block_64.break_into_sub_blocks(2)
            for i in range(8):
                sub_block_16 = round(sub_block_16, self.generate_sub_keys(i * 6))
            last_cipher_block = Block.join(final_round(sub_block_16, self.generate_sub_keys(8 * 6)))
            cipher_text += last_cipher_block.data
        return cipher_text
