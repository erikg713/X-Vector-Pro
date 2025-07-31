import socket
import requests
import subprocess
from datetime import datetime
from core.logger import log_event

log_event("scan", {"target": "localhost"}, level="debug", write_structured_file=True)
from core.recon.subdomain_enum import SubdomainEnum
from core.recon.port_scan import PortScanner
from core.recon.http_header_collector import HTTPHeaderCollector

domain = "example.com"
sub_enum = SubdomainEnum(domain)
print("Found subdomains:", sub_enum.run())

scanner = PortScanner("93.184.216.34")  # example.com IP
print("Open ports:", scanner.run())

header_collector = HTTPHeaderCollector("http://example.com")
print("HTTP Headers:", header_collector.collect_headers())


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
from core.logger import log_event

log_event("scan", {"target": "localhost"}, level="debug", write_structured_file=True)
