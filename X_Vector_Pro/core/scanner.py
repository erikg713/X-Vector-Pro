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
