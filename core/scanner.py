import socket
import requests
from utils.logger import log  # Ensure consistent logging

# Configuration
DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389, 8080]
DEFAULT_DIRB_PATHS = ["admin", "wp-login", "phpmyadmin"]

def port_scan(host, ports=None):
    """
    Perform a TCP port scan on a target host.

    Args:
        host (str): The target IP or hostname to scan.
        ports (list): List of ports to scan. Defaults to common ports.

    Returns:
        list: A list of strings describing the status of each port.
    """
    if ports is None:
        ports = DEFAULT_PORTS

    log(f"[*] Starting port scan on {host}")
    results = []

    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=1):
                results.append(f"[+] Port {port} is OPEN")
                log(f"[+] Port {port} is OPEN")
        except Exception as e:
            results.append(f"[-] Port {port} is closed or filtered ({e})")
            log(f"[-] Port {port} is closed or filtered ({e})")

    return results


def dirb_scan(base_url, paths=None):
    """
    Perform a simple directory brute-force scan on a target URL.

    Args:
        base_url (str): The base URL to scan.
        paths (list): List of paths to check. Defaults to common paths.

    Returns:
        list: A list of found paths with HTTP 200 status.
    """
    if paths is None:
        paths = DEFAULT_DIRB_PATHS

    log(f"[*] Starting directory brute-force scan on {base_url}")
    results = []

    for path in paths:
        try:
            url = f"{base_url}/{path}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results.append(f"[+] Found: {url}")
                log(f"[+] Found: {url}")
        except Exception as e:
            log(f"[!] Error accessing {url}: {e}")

    return results


if __name__ == "__main__":
    # Example usage
    target_host = "127.0.0.1"
    target_url = "http://example.com"

    # Port Scan Example
    scan_results = port_scan(target_host)
    print("\n".join(scan_results))

    # Directory Brute-Force Example
    dirb_results = dirb_scan(target_url)
    print("\n".join(dirb_results))
