# core/recon.py

import socket
import subprocess
import platform
from datetime import datetime

try:
    import whois
except ImportError:
    whois = None  # Optional dependency

def resolve_dns(target):
    try:
        ip = socket.gethostbyname(target)
        return f"[+] DNS Resolved: {target} → {ip}", ip
    except socket.gaierror:
        return f"[!] DNS Resolution Failed for {target}", target

def ping_host(ip):
    ping_cmd = ["ping", "-n", "1", ip] if platform.system() == "Windows" else ["ping", "-c", "1", ip]
    try:
        subprocess.check_output(ping_cmd, stderr=subprocess.DEVNULL)
        return f"[+] Ping: Host {ip} is reachable"
    except subprocess.CalledProcessError:
        return f"[!] Ping: Host {ip} is unreachable"

def guess_os(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            sock.settimeout(2)
            sock.sendto(b"\x08\x00\x7d\x4b\x00\x01\x00\x01", (ip, 1))
            _, addr = sock.recvfrom(1024)
            if addr:
                return "[+] OS Fingerprint: Likely Unix/Linux (low TTL)"
    except:
        pass
    return "[*] OS Fingerprint: Could not determine (raw socket failed or blocked)"

def scan_ports(ip, ports=[21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]):
    open_ports = []
    output = ["[*] Port Scan Results:"]
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.3)
            try:
                sock.connect((ip, port))
                open_ports.append(port)
                output.append(f"    [+] Port {port} open")
            except:
                pass
    return "\n".join(output), open_ports

def grab_banner(ip, port):
    try:
        with socket.socket() as sock:
            sock.settimeout(1)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return f"[+] Banner ({port}): {banner}"
    except:
        return f"[*] Banner ({port}): No response"

def perform_whois(target):
    if not whois:
        return "[*] WHOIS: Skipped (python-whois not installed)"
    try:
        domain_info = whois.whois(target)
        return f"[+] WHOIS:\n    - Registrar: {domain_info.registrar}\n    - Country: {domain_info.country}"
    except Exception as e:
        return f"[!] WHOIS Failed: {e}"

def run_auto_recon(target="127.0.0.1"):
    output = []
    output.append(f"--- Auto Recon Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    output.append(f"Target: {target}")

    # DNS
    dns_msg, ip = resolve_dns(target)
    output.append(dns_msg)

    # Ping
    output.append(ping_host(ip))

    # OS Fingerprinting
    output.append(guess_os(ip))

    # Port Scan
    port_msg, open_ports = scan_ports(ip)
    output.append(port_msg)

    # Banner Grabbing
    for port in open_ports:
        output.append(grab_banner(ip, port))

    # WHOIS
    output.append(perform_whois(target))

    output.append("--- Recon Complete ---")
    return "\n".join(output)
