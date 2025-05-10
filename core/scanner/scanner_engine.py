# core/scanner/scanner_engine.py
import requests
import socket
from queue import Queue
import threading

def run_dir_scan(url, output_box):
    if not url.startswith("http"):
        output_box.insert("end", "[!] Invalid URL. Use full http/https.\n")
        return

    output_box.insert("end", "[*] Starting directory scan...\n")
    wordlist = ["admin", "login", "dashboard", "wp-admin", "config", "backup", "phpmyadmin"]

    def scan_path(path):
        try:
            full_url = f"{url.rstrip('/')}/{path}"
            r = requests.get(full_url, timeout=5)
            if r.status_code in [200, 301, 403]:
                output_box.insert("end", f"[+] {full_url} [{r.status_code}]\n")
        except Exception:
            pass

    threads = []
    for path in wordlist:
        t = threading.Thread(target=scan_path, args=(path,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    output_box.insert("end", "[*] Directory scan completed.\n")

def run_port_scan(target, output_box):
    output_box.insert("end", f"[*] Starting port scan on {target}...\n")
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8080]
    q = Queue()

    for port in ports:
        q.put(port)

    def worker():
        while not q.empty():
            port = q.get()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    if s.connect_ex((target, port)) == 0:
                        output_box.insert("end", f"[+] Open port: {port}\n")
            except:
                pass
            q.task_done()

    for _ in range(50):
        threading.Thread(target=worker, daemon=True).start()

    q.join()
    output_box.insert("end", "[*] Port scan complete.\n")
