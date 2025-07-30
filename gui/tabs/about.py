X-Vector Pro Overview
X-Vector Pro is a tactical, GUI-driven WordPress security tool that automates:

Reconnaissance and subdomain enumeration

Plugin and theme scanning for vulnerable versions

Brute-force password attacks against WordPress logins

CVE detection and exploitation

Comprehensive HTML and JSON reporting

Quick Start
bash
Copy
Edit
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py --auto --target https://example.com
Core Features
Auto Mode: Runs full recon → scan → brute → CVE check → exploit pipeline

Plugin Scanner: Enumerate installed plugins/themes and flag outdated versions

Brute Force Module: Target WordPress logins with customizable password lists

CVE Lookup: Detect local CVEs against your target plugins/themes

Reporting: Generates detailed HTML & JSON reports saved to the reports/ directory

Architecture Layers
GUI Layer: CustomTkinter-based tab UI

CLI Interface: Flexible argument parsing for automation

Controller Layer: Orchestrates all scanning and exploitation modules

Core Modules: Recon, scanning, brute forcing, CVE detection, exploitation

Reporting Engine: Generates HTML/PDF reports from results

If you want, I can also generate you the core folder code files (like controller, recon, scanner modules), or the full GUI code, or help build plugin scan and brute force modules in Python. Just say what part you want next!








Ask ChatGPT
You said:
go


ChatGPT said:
Alright, here’s a clean, foundational core module setup for X-Vector Pro to get you started with the main orchestration and scanning pipeline in Python:

core/controller.py
python
Copy
Edit
import threading
from recon.subdomain_enum import SubdomainEnum
from scanner.plugin_scanner import PluginScanner
from brute.password_brute import BruteEngine
from core.cve_scanner import CVEScanner

class XVectorController:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def run_recon(self):
        recon = SubdomainEnum(self.target)
        subdomains = recon.run()
        self.results['subdomains'] = subdomains
        return subdomains

    def run_plugin_scan(self):
        scanner = PluginScanner(self.target)
        plugins = scanner.scan()
        self.results['plugins'] = plugins
        return plugins

    def run_brute_force(self):
        brute = BruteEngine(self.target)
        brute.load_wordlist('data/wordlists/passwords.txt')
        brute.start()
        self.results['brute'] = 'Completed'
        return 'Brute force completed'

    def run_cve_check(self):
        cve = CVEScanner(self.target)
        found_cves = cve.scan()
        self.results['cves'] = found_cves
        return found_cves

    def run_full_pipeline(self):
        self.run_recon()
        self.run_plugin_scan()
        self.run_brute_force()
        self.run_cve_check()
        return self.results
recon/subdomain_enum.py
python
Copy
Edit
import requests

class SubdomainEnum:
    def __init__(self, target):
        self.target = target

    def run(self):
        # Simplified enumeration example
        subdomains = ['www', 'blog', 'shop']
        found = []
        for sub in subdomains:
            url = f"http://{sub}.{self.target}"
            try:
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    found.append(url)
            except:
                continue
        return found
scanner/plugin_scanner.py
python
Copy
Edit
class PluginScanner:
    def __init__(self, target):
        self.target = target

    def scan(self):
        # Dummy data, replace with real detection logic
        return {
            'akismet': '4.1',
            'yoast-seo': '15.2'
        }
brute/password_brute.py
python
Copy
Edit
import time

class BruteEngine:
    def __init__(self, target):
        self.target = target
        self.wordlist = []

    def load_wordlist(self, path):
        with open(path, 'r') as f:
            self.wordlist = [line.strip() for line in f.readlines()]

    def start(self):
        # Simulate brute forcing
        for pwd in self.wordlist[:10]:  # Just test 10 for demo
            print(f"Trying password: {pwd} on {self.target}")
            time.sleep(0.2)  # Simulate delay
core/cve_scanner.py
python
Copy
Edit
class CVEScanner:
    def __init__(self, target):
        self.target = target

    def scan(self):
        # Dummy CVE check
        return [
            {'plugin': 'akismet', 'cve_id': 'CVE-2023-1234', 'severity': 'high'},
        ]
How to run:
python
Copy
Edit
from core.controller import XVectorController

target = "example.com"
controller = XVectorController(target)
results = controller.run_full_pipeline()
print(results)
This basic setup gives you modular layers to extend for real scanning, recon, brute-force, and CVE detection.

Want me to generate GUI integration next or dive deeper into any module?







