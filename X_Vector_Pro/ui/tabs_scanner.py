# ui/tabs_scanner.py
import customtkinter as ctk
import threading, socket, requests
from tkinter import messagebox
from queue import Queue

def load_scanner_tab(tab):
    def run_port_scan():
        target = scanner_target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a valid target IP or domain.")
            return

        scanner_output.delete("0.0", "end")
        scanner_output.insert("end", f"[*] Starting port scan on {target}...\n")

        def scan_worker():
            while not q.empty():
                port = q.get()
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)
                        if s.connect_ex((target, port)) == 0:
                            scanner_output.insert("end", f"[+] Port {port} is open\n")
                except Exception as e:
                    scanner_output.insert("end", f"[-] Error on port {port}: {e}\n")
                q.task_done()

        top_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
                     1723, 3306, 3389, 5900, 8080, 8443, 8888, 8000, 8081, 8880, 10000, 9200,
                     5432, 389, 137, 138, 139, 2049, 1521, 465, 993, 995, 1025, 49152, 49153]

        q = Queue()
        for port in top_ports:
            q.put(port)

        for _ in range(100):
            threading.Thread(target=scan_worker, daemon=True).start()

        q.join()
        scanner_output.insert("end", "[*] Port scan finished.\n")

    def run_dir_scan():
        url = scanner_target_entry.get().strip().rstrip("/")
        if not url.startswith("http"):
            messagebox.showerror("Error", "Use full URL (http/https).")
            return

        scanner_output.insert("end", "\n[*] Starting directory scan...\n")

        wordlist = ["admin", "login", "dashboard", "config", "backup", "wp-admin",
                    "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"]

        def scan_path(path):
            full_url = f"{url}/{path}"
            try:
                r = requests.get(full_url, timeout=5)
                if r.status_code in [200, 301, 403]:
                    scanner_output.insert("end", f"[+] {full_url} [{r.status_code}]\n")
            except Exception:
                pass

        threads = []
        for path in wordlist:
            t = threading.Thread(target=scan_path, args=(path,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        scanner_output.insert("end", "[*] Dir scan finished.\n")

    ctk.CTkLabel(tab, text="Target IP or Domain").pack(pady=5)
    scanner_target_entry = ctk.CTkEntry(tab, width=500)
    scanner_target_entry.pack()

    ctk.CTkButton(tab, text="Start Port Scan", command=lambda: threading.Thread(target=run_port_scan).start()).pack(pady=5)
    ctk.CTkButton(tab, text="Start Dir Scan", command=lambda: threading.Thread(target=run_dir_scan).start()).pack(pady=5)

    scanner_output = ctk.CTkTextbox(tab, height=400, width=800)
    scanner_output.pack()
