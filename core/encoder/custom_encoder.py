class CustomEncoder:
    def encode(self, data: str, key: int = 3) -> str:
        return ''.join(chr((ord(c) + key) % 256) for c in data)

    def decode(self, data: str, key: int = 3) -> str:
        return ''.join(chr((ord(c) - key) % 256) for c in data)

# Example
if __name__ == "__main__":
    encoder = CustomEncoder()
    secret = encoder.encode("payload123", key=7)
    print("Encoded:", secret)
    print("Decoded:", encoder.decode(secret, key=7))
