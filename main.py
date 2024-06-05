from cryptography.algorithm import MyCryptoAlgorithm


def main():
    plain_text = b'Hello, World!'
    key = b'1234567890abcdef'
    c = MyCryptoAlgorithm(plain_text, key)
    print(c.encrypt())
    print(c.CBC_encrypt())
    print(c.CTR_encrypt())


if __name__ == '__main__':
    main()
