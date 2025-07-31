import base64

def decode_b64(data: str) -> str:
    try:
        return base64.b64decode(data).decode('utf-8')
    except Exception as e:
        return str(e)
