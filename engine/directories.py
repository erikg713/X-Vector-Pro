# X_Vector_Pro/engine/dirs.py

"""
Directory Scanner for X-Vector Pro

Performs common directory brute-forcing against a base URL.
Supports wordlist override, stealth delays, and structured logging.
"""

import requests
from utils.logger import log_to_central
from utils.stealth import stealth_delay

class DirectoryScanner:
    def __init__(self, base_url, logger=log_to_central, wordlist=None, config=None):
        self.url = base_url.rstrip("/")
        self.log = logger
        self.config = config or {}
        self.wordlist = wordlist or [
            "admin", "login", "wp-admin", "config", "dashboard", "cpanel", 
            ".git", ".env", "server-status", "backup", "uploads", "phpmyadmin"
        ]

    def run(self, findings=None, update_callback=None):
        self.log("[*] Running Directory Scan...")
        if findings is not None and "directories" not in findings:
            findings["directories"] = []

        headers = {}
        if self.config.get("random_user_agent"):
            from utils.helpers import get_random_user_agent
            headers["User-Agent"] = get_random_user_agent()

        for path in self.wordlist:
            target = f"{self.url}/{path}"
            try:
                r = requests.get(target, headers=headers, timeout=4, allow_redirects=False)
                code = r.status_code
                if code in [200, 301, 302, 403]:
                    if findings is not None:
                        findings["directories"].append({"path": target, "code": code})
                    self.log(f"    [+] Found: {target} [{code}]")
                    if update_callback:
                        update_callback(f"[+] Directory: {target} ({code})")
            except requests.RequestException:
                self.log(f"    [!] Timeout or connection error on: {target}")
            stealth_delay(self.config)

        self.log("[*] Directory Scan Completed.")
