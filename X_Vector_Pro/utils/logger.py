from datetime import datetime
from cryptography.fernet import Fernet

def encrypt_log(data: str, output_path: str):
      key = Fernet.generate_key()
      cipher_suite = Fernet(key)
      encrypted_data = cipher_suite.encrypt(data.encode())

      with open(output_path, 'wb') as f:
          f.write(encrypted_data)


def log(msg):
    with open("xvector_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

def save_hit(username, password):
    hit = f"{username}:{password}"
    with open("hits.txt", "a") as f:
        f.write(f"{hit}\n")
    log(f"[+] Valid credentials found: {hit}")
