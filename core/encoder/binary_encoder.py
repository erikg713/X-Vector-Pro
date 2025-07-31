class BinaryEncoder:
    def encode(self, data: str) -> str:
        return ' '.join(format(ord(char), '08b') for char in data)

    def decode(self, binary: str) -> str:
        return ''.join(chr(int(b, 2)) for b in binary.split())

# Example
if __name__ == "__main__":
    encoder = BinaryEncoder()
    binary = encoder.encode("root")
    print("Binary:", binary)
    print("Decoded:", encoder.decode(binary))
