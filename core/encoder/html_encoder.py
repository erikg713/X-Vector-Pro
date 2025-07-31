import html

class HTMLEncoder:
    def encode(self, data: str) -> str:
        return html.escape(data)

    def decode(self, encoded: str) -> str:
        return html.unescape(encoded)

# Example
if __name__ == "__main__":
    e = HTMLEncoder()
    s = '<script>alert("XSS")</script>'
    print("Encoded:", e.encode(s))
    print("Decoded:", e.decode(e.encode(s)))
