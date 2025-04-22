 core/scanner.py
def run_port_scan(target):
    return f"Scan on {target}: Port 80 open (Fake result)"

def run_port_scan(target, ports=[22, 80, 443, 8080]):
    result = []
    for port in ports:
        try:
            with socket.create_connection((target, port), timeout=1):
                result.append(f"Port {port} is open")
        except:
            result.append(f"Port {port} is closed or filtered")
    return "\n".join(result)

import socket
import requests
from utils.logger import log

def port_scan(host, ports=[21, 22, 80, 443, 3306]):
    log(f"[*] Scanning ports on {host}")
    for port in ports:
        try:
            s = socket.create_connection((host, port), timeout=1)
            log(f"[+] Port {port} is OPEN")
            s.close()
        except:
            pass

def dirb_scan(base_url, paths=["admin", "wp-login", "phpmyadmin"]):
    log(f"[*] Starting DirBuster scan on {base_url}")
    for path in paths:
        try:
            url = f"{base_url}/{path}"
            r = requests.get(url)
            if r.status_code == 200:
                log(f"[+] Found: {url}")
        except:
            pass
import socket
import requests
from utils.logger import log

def port_scan(host, ports=[21, 22, 80, 443, 3306]):
    log(f"[*] Scanning ports on {host}")
    for port in ports:
        try:
            s = socket.create_connection((host, port), timeout=1)
            log(f"[+] Port {port} is OPEN")
            s.close()
        except:
            pass

def dirb_scan(base_url, paths=["admin", "wp-login", "phpmyadmin"]):
    log(f"[*] Starting DirBuster scan on {base_url}")
    for path in paths:
        try:
            url = f"{base_url}/{path}"
            r = requests.get(url)
            if r.status_code == 200:
                log(f"[+] Found: {url}")
        except:
            pass
