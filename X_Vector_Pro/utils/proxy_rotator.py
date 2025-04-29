import random
import requests
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def load_proxies(file_path="proxies.txt"):
    try:
        with open(file_path, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            raise ValueError("Proxy list is empty.")
        return proxies
    except Exception as e:
        print(f"[ProxyRotator] Failed to load proxies: {e}")
        return []

def request_with_random_proxy(url, method="GET", data=None, headers=None, timeout=10, proxies_list=None):
    if proxies_list is None:
        proxies_list = load_proxies()

    if not proxies_list:
        raise ValueError("No proxies available.")

    proxy = random.choice(proxies_list)
    proxy_dict = {
        "http": proxy,
        "https": proxy
    }

    session = requests.Session()
    session.proxies.update(proxy_dict)

    try:
        if method.upper() == "GET":
            response = session.get(url, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = session.post(url, data=data, headers=headers, timeout=timeout)
        else:
            raise ValueError("Unsupported method.")
        return response
    except Exception as e:
        print(f"[ProxyRotator] Request failed with proxy {proxy}: {e}")
        raise
