import requests
import socket
from utils.logger import log

def basic_recon(target_url):
    log("[*] Starting recon...")

    try:
        ip = socket.gethostbyname(target_url.replace("http://", "").replace("https://", "").split("/")[0])
        headers = requests.get(target_url).headers
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
    except Exception as e:
        log(f"[!] Recon failed: {e}")
        return

    log(f"[+] IP Address: {ip}")
    log(f"[+] Server: {server}")
    log(f"[+] X-Powered-By: {powered_by}")
