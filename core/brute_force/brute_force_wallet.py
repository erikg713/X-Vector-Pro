import json
import getpass
from eth_keyfile import load_keyfile, decode_keyfile_json
from pathlib import Path

def try_passwords(wallet_path, wordlist_path):
    with open(wallet_path, 'rb') as f:
        keyfile_json = json.load(f)

    with open(wordlist_path, 'r', encoding='latin-1') as wordlist:
        for i, password in enumerate(wordlist):
            password = password.strip()
            try:
                private_key = decode_keyfile_json(keyfile_json, password.encode('utf-8'))
                print(f"[+] SUCCESS! Password found: {password}")
                print(f"[+] Private key: 0x{private_key.hex()}")
                return password
            except Exception as e:
                if i % 1000 == 0:
                    print(f"[-] Tried {i} passwords...")
                continue

    print("[-] No matching password found.")
    return None

def main():
    print("==== Coinbase Wallet Brute Force Recovery ====")
    wallet_file = input("Enter path to wallet JSON file (e.g. wallet1.json): ").strip()
    wordlist_file = input("Enter path to wordlist (e.g. rockyou.txt): ").strip()

    if not Path(wallet_file).is_file() or not Path(wordlist_file).is_file():
        print("[!] File not found.")
        return

    try_passwords(wallet_file, wordlist_file)

if __name__ == "__main__":
    main()