class XOREncoder:
    def encode(self, text: str, key: int) -> str:
        return ''.join(chr(ord(c) ^ key) for c in text)

    def decode(self, encoded: str, key: int) -> str:
        return ''.join(chr(ord(c) ^ key) for c in encoded)

# Example
if __name__ == "__main__":
    xor = XOREncoder()
    encoded = xor.encode("stealth", 42)
    print("Encoded:", encoded)
    print("Decoded:", xor.decode(encoded, 42))
