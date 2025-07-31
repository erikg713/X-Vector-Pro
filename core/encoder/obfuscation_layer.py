from base64 import b64encode

class ObfuscationLayer:
    def layer(self, payload: str, times: int = 3) -> str:
        for _ in range(times):
            payload = b64encode(payload.encode()).decode()
        return payload

# Example
if __name__ == "__main__":
    ol = ObfuscationLayer()
    layered = ol.layer("exec('/bin/bash')", 4)
    print("Obfuscated:", layered)
