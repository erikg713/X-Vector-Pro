import requests

def brute_dirs(url: str, wordlist: list) -> list:
    found = []
    for word in wordlist:
        full_url = f"{url.rstrip('/')}/{word}"
        resp = requests.get(full_url)
        if resp.status_code < 400:
            found.append(full_url)
    return found
