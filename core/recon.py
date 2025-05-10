# core/recon.py

import socket
import subprocess
import platform
from datetime import datetime

def run_auto_recon(target="127.0.0.1"):
    """
    Performs basic recon: DNS lookup, ping check, and basic port scan.
    Returns a formatted string report.
    """
    result = []
    result.append(f"--- Auto Recon Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    result.append(f"Target: {target}")
    
    # DNS resolution
    try:
        ip = socket.gethostbyname(target)
        result.append(f"[+] DNS Resolved: {target} → {ip}")
    except socket.gaierror:
        result.append(f"[!] DNS Resolution Failed for {target}")
        ip = target  # fallback

    # Ping check
    ping_cmd = ["ping", "-n", "1", ip] if platform.system() == "Windows" else ["ping", "-c", "1", ip]
    try:
        subprocess.check_output(ping_cmd, stderr=subprocess.DEVNULL)
        result.append(f"[+] Ping: Host {ip} is reachable")
    except subprocess.CalledProcessError:
        result.append(f"[!] Ping: Host {ip} is unreachable")

    # Basic port scan (top 10 ports)
    common_ports = [22, 23, 80, 443, 445, 21, 25, 53, 110, 3389]
    result.append("[*] Scanning Top 10 Common Ports:")
    for port in common_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                sock.connect((ip, port))
                result.append(f"    [+] Port {port} open")
            except:
                pass  # ignore closed ports

    result.append("--- Recon Complete ---")
    return "\n".join(result)
