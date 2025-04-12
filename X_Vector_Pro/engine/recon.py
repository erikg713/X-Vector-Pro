# engine/recon.py
import requests

class ReconScanner:
    def __init__(self, url, logger):
        self.url = url
        self.log = logger

    def run(self, findings=None):
        try:
            self.log("[*] Running Recon...")
            r = requests.get(self.url, timeout=10)
            if "<title>" in r.text:
                title = r.text.split("<title>")[1].split("</title>")[0].strip()
                if findings is not None:
                    findings["title"] = title
                self.log(f"    [+] Site title: {title}")
        except Exception as e:
            self.log(f"[!] Recon failed: {e}")
