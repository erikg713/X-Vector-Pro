import urllib.parse

class URLDecoder:
    def __init__(self):
        pass

    def decode_url(self, encoded_url: str) -> str:
        return urllib.parse.unquote(encoded_url)

# Example usage
if __name__ == "__main__":
    decoder = URLDecoder()
    obfuscated = "https%3A%2F%2Fevil.example.com%2Fshell%3Fid%3Droot"
    print("Decoded:", decoder.decode_url(obfuscated))
