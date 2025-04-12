from datetime import datetime

def log(msg):
    with open("xvector_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

from datetime import datetime

def log(msg):
    with open("xvector_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def save_hit(username, password):
    hit = f"{username}:{password}"
    with open("hits.txt", "a") as f:
        f.write(f"{hit}\n")
    log(f"[+] Valid credentials found: {hit}")
