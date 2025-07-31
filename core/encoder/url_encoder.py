import urllib.parse

class URLEncoder:
    def encode(self, data: str) -> str:
        return urllib.parse.quote_plus(data)

    def decode(self, encoded: str) -> str:
        return urllib.parse.unquote_plus(encoded)

# Example
if __name__ == "__main__":
    encoder = URLEncoder()
    test = "param=1&evil=<script>"
    encoded = encoder.encode(test)
    print("Encoded:", encoded)
    print("Decoded:", encoder.decode(encoded))
