from cryptography.algorithm import MMA


def main():
    plain_text = b'Hello, World!'
    key = b'1234567890abcdef'
    mma = MMA(plain_text, key)
    print(mma.encrypt())
    print(mma.CBC_encrypt())
    print(mma.CTR_encrypt())


if __name__ == '__main__':
    main()
