import socket
import subprocess
import requests
import time
import json
import os

# ------------- Logger -------------
def log_event(category, data, level="INFO"):
    log_line = f"[{level}] {category} | {json.dumps(data)}"
    print(log_line)
    with open("xvector_log.txt", "a") as f:
        f.write(log_line + "\n")


# ------------- Recon Engine -------------
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
        log_event("recon", {"step": "start", "target": self.target})
        self.resolve_ip()
        self.http_headers()
        self.whois_lookup()
        log_event("recon", {"step": "complete", "results": self.results})
        return self.results


# ------------- Plugin Scanner -------------
class PluginScanner:
    def __init__(self, target):
        self.target = target

    def scan(self):
        log_event("plugin_scan", {"step": "start", "target": self.target})
        # Dummy plugins
        plugins = {"akismet": "4.1", "yoast-seo": "15.2"}
        log_event("plugin_scan", {"step": "complete", "plugins": plugins})
        return plugins


# ------------- Brute Force Engine -------------
class BruteEngine:
    def __init__(self, target):
        self.target = target
        self.wordlist = []

    def load_wordlist(self, path):
        try:
            with open(path, "r") as f:
                self.wordlist = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            self.wordlist = ["admin", "password", "123456"]

    def start(self):
        log_event("brute_force", {"step": "start", "target": self.target})
        for pwd in self.wordlist[:5]:  # Simulate only top 5
            print(f"Trying password: {pwd}")
            time.sleep(0.2)
        log_event("brute_force", {"step": "complete"})


# ------------- CVE Scanner -------------
class CVEScanner:
    def __init__(self, target, plugins):
        self.target = target
        self.plugins = plugins

    def scan(self):
        log_event("cve_scan", {"step": "start"})
        cves = []
        if "akismet" in self.plugins:
            cves.append({
                "plugin": "akismet",
                "cve_id": "CVE-2023-1234",
                "severity": "HIGH"
            })
        log_event("cve_scan", {"step": "complete", "found": cves})
        return cves


# ------------- Controller -------------
class XVectorController:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def run_recon(self):
        recon = ReconEngine(self.target)
        self.results["recon"] = recon.run_full_recon()

    def run_plugin_scan(self):
        scanner = PluginScanner(self.target)
        self.results["plugins"] = scanner.scan()

    def run_brute_force(self):
        brute = BruteEngine(self.target)
        brute.load_wordlist("passwords.txt")
        brute.start()
        self.results["brute"] = "completed"

    def run_cve_check(self):
        plugins = self.results.get("plugins", {})
        cve = CVEScanner(self.target, plugins)
        self.results["cves"] = cve.scan()

    def run_full_pipeline(self):
        log_event("controller", {"action": "pipeline_start", "target": self.target})
        self.run_recon()
        self.run_plugin_scan()
        self.run_brute_force()
        self.run_cve_check()
        log_event("controller", {"action": "pipeline_complete", "results": self.results})
        return self.results


# ------------- Entry Point -------------
if __name__ == "__main__":
    target = input("Enter target domain: ").strip()
    controller = XVectorController(target)
    results = controller.run_full_pipeline()

    print("\n=== Final Results ===")
    print(json.dumps(results, indent=2))

    # Save structured report
    with open("xvector_report.json", "w") as f:
        json.dump(results, f, indent=2)
