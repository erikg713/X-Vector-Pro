import base64
import binascii
import re

class EncodingDetector:
    def is_base64(self, s: str) -> bool:
        try:
            return base64.b64encode(base64.b64decode(s)).decode() == s
        except Exception:
            return False

    def is_hex(self, s: str) -> bool:
        try:
            int(s, 16)
            return len(s) % 2 == 0
        except ValueError:
            return False

    def detect(self, payload: str) -> str:
        payload = payload.strip().replace(" ", "")
        if self.is_base64(payload):
            return "base64"
        elif self.is_hex(payload):
            return "hex"
        else:
            return "unknown"

# Example usage
if __name__ == "__main__":
    detector = EncodingDetector()
    print(detector.detect("48656c6c6f20776f726c64"))
    print(detector.detect("SGVsbG8gd29ybGQ="))
