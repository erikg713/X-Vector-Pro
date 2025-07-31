import requests

def fetch_headers(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=3)
        return dict(resp.headers)
    except Exception as e:
        return {"error": str(e)}
