from typing import Generator

from idea.base.data import Block
from idea.algorithm.round import round, final_round


class IDEA:
    def __init__(self, plain_text:bytes) -> None:
        if w := len(plain_text) % 8 == 0:
            zero_padding = bytearray(0)
        else:
            zero_padding = bytearray(8 - w)
        self.plain_text = plain_text + zero_padding

    def generate_blocks_64bits(self) -> Generator[Block, None, None]:
        for i in range(0, len(self.plain_text), 8):
            yield Block(self.plain_text[i:i + 8])

    def encrypt(self) -> bytes:
        cipher_text = b''
        for block_64 in self.generate_blocks_64bits():
            sub_block_16 = (block_64[0:2], block_64[2:4], block_64[4:6], block_64[6:8])
            for _ in range(8):
                sub_block_16 = round(sub_block_16, None)
            cipher_text += b''.join(final_round(sub_block_16, None))
        return cipher_text
