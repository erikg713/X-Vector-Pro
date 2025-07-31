import base64

class Base64Encoder:
    def encode(self, data: str) -> str:
        return base64.b64encode(data.encode()).decode()

    def decode(self, encoded: str) -> str:
        return base64.b64decode(encoded.encode()).decode()

# Example
if __name__ == "__main__":
    encoder = Base64Encoder()
    data = "Hello, world!"
    encoded = encoder.encode(data)
    print("Encoded:", encoded)
    print("Decoded:", encoder.decode(encoded))
