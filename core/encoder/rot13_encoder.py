import codecs

class ROT13Encoder:
    def encode(self, data: str) -> str:
        return codecs.encode(data, 'rot_13')

    def decode(self, encoded: str) -> str:
        return codecs.decode(encoded, 'rot_13')

# Example
if __name__ == "__main__":
    e = ROT13Encoder()
    text = "exploit"
    r = e.encode(text)
    print("ROT13:", r)
    print("Back:", e.decode(r))
