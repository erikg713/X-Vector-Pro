import socket
from core.logger import log_event

def run_port_scan(target, ports=None):
    # ... existing scan logic ...
    result_text = "\n".join(results)

    log_event("scan", {
        "target": target,
        "results": results
    })

    return result_text
def run_port_scan(target, ports=None):
    """
    Basic TCP port scanner.

    Args:
        target (str): IP or hostname to scan.
        ports (list): List of ports to scan. Defaults to common ports.

    Returns:
        str: Formatted scan result.
    """
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

    results = [f"[SCAN] Starting scan on {target}...\n"]

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                results.append(f"[+] Port {port} is OPEN")
            else:
                results.append(f"[-] Port {port} is closed")
            sock.close()
        except Exception as e:
            results.append(f"[!] Error scanning port {port}: {str(e)}")

    return "\n".join(results)
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
