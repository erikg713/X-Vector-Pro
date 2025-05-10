import socket
import requests
import subprocess
from datetime import datetime

class ReconEngine:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def resolve_ip(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.results["resolved_ip"] = ip
            return ip
        except socket.gaierror:
            self.results["resolved_ip"] = None
            return None

    def whois_lookup(self):
        try:
            result = subprocess.check_output(["whois", self.target], text=True, timeout=10)
            self.results["whois"] = result
            return result
        except Exception as e:
            self.results["whois"] = str(e)
            return str(e)

    def http_headers(self):
        try:
            response = requests.get(f"http://{self.target}", timeout=5)
            self.results["headers"] = dict(response.headers)
            return response.headers
        except Exception as e:
            self.results["headers"] = str(e)
            return str(e)

    def run_full_recon(self):
        print(f"[+] Starting recon on: {self.target}")
        self.resolve_ip()
        self.http_headers()
        self.whois_lookup()
        print("[+] Recon complete.")
        return self.results
