# engine/dirs.py
import requests

class DirectoryScanner:
    def __init__(self, base_url, logger):
        self.url = base_url.rstrip("/")
        self.log = logger
        self.common_dirs = ["admin", "login", "wp-admin", "config"]

    def run(self, findings=None):
        self.log("[*] Running Directory Scan...")
        for path in self.common_dirs:
            check = f"{self.url}/{path}"
            try:
                r = requests.get(check, timeout=3)
                if r.status_code in [200, 301, 403]:
                    if findings is not None:
                        findings["directories"].append({"path": check, "code": r.status_code})
                    self.log(f"    [+] Found: {check} [{r.status_code}]")
            except:
                continue
