class HexEncoder:
    def encode(self, data: str) -> str:
        return data.encode().hex()

    def decode(self, encoded: str) -> str:
        return bytes.fromhex(encoded).decode()

# Example
if __name__ == "__main__":
    encoder = HexEncoder()
    data = "Attack"
    hexed = encoder.encode(data)
    print("Hex:", hexed)
    print("Decoded:", encoder.decode(hexed))
