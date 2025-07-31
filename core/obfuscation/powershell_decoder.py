import base64
import re

class PowerShellDecoder:
    def decode_base64_command(self, command: str) -> str:
        match = re.search(r'(?i)-enc(?:odedcommand)?\s+([A-Za-z0-9+/=]+)', command)
        if match:
            b64_payload = match.group(1)
            try:
                decoded = base64.b64decode(b64_payload).decode('utf-16le')
                return decoded
            except Exception as e:
                return f"Error decoding: {e}"
        return "No encoded PowerShell command found."

# Example usage
if __name__ == "__main__":
    ps_cmd = "powershell -encodedCommand UwB0AGEAcgB0AC0AUAByAG8AYwBlAHMAcwA="
    decoder = PowerShellDecoder()
    print("Decoded Command:", decoder.decode_base64_command(ps_cmd))
