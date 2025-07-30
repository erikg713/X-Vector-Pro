import requests

class ReconEngine:
    def __init__(self, target):
        self.target = target.rstrip('/')

    def run(self):
        # Simple subdomain enumeration example
        subdomains = ['www', 'mail', 'ftp', 'test']
        found = []

        for sub in subdomains:
            url = f"http://{sub}.{self.target}"
            try:
                resp = requests.head(url, timeout=3)
                if resp.status_code < 400:
                    found.append(url)
            except Exception:
                continue
        return found

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
