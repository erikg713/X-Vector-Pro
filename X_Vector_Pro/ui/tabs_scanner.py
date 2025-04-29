import customtkinter as ctk
import threading, socket, requests
from tkinter import messagebox
from queue import Queue
import time

def load_scanner_tab(tab):
    def run_port_scan():
        target = scanner_target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a valid target IP or domain.")
            return

        scanner_output.delete("0.0", "end")
        scanner_output.insert("end", f"[*] Starting port scan on {target}...\n")
        status_label.configure(text="Status: Scanning...", fg="#28A745")

        def scan_worker():
            while not q.empty():
                port = q.get()
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)  # Timeout for each port scan
                        if s.connect_ex((target, port)) == 0:
                            scanner_output.insert("end", f"[+] Port {port} is open\n", "green")
                        else:
                            scanner_output.insert("end", f"[-] Port {port} is closed\n", "red")
                except Exception as e:
                    scanner_output.insert("end", f"[-] Error on port {port}: {e}\n", "yellow")
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
        status_label.configure(text="Status: Scan Complete", fg="#007BFF")

    def run_dir_scan():
        url = scanner_target_entry.get().strip().rstrip("/")
        if not url.startswith("http"):
            messagebox.showerror("Error", "Use full URL (http/https).")
            return

        scanner_output.insert("end", "\n[*] Starting directory scan...\n")
        status_label.configure(text="Status: Scanning directories...", fg="#28A745")

        wordlist = ["admin", "login", "dashboard", "config", "backup", "wp-admin",
                    "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"]

        def scan_path(path):
            full_url = f"{url}/{path}"
            try:
                r = requests.get(full_url, timeout=5)
                if r.status_code in [200, 301, 403]:
                    scanner_output.insert("end", f"[+] {full_url} [{r.status_code}]\n", "green")
                else:
                    scanner_output.insert("end", f"[-] {full_url} [{r.status_code}]\n", "red")
            except Exception:
                scanner_output.insert("end", f"[-] Error with path {full_url}\n", "yellow")

        threads = []
        for path in wordlist:
            t = threading.Thread(target=scan_path, args=(path,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        scanner_output.insert("end", "[*] Dir scan finished.\n")
        status_label.configure(text="Status: Directory Scan Complete", fg="#007BFF")

    # Header section with blue background color and padding
    header_frame = ctk.CTkFrame(tab, height=50, corner_radius=10, bg_color="#007BFF")  # Blue color
    header_frame.pack(fill="x", pady=(10, 5))

    # Title label inside the header with white text
    title_label = ctk.CTkLabel(header_frame, text="Scanner Tool", font=("Roboto", 20, "bold"), fg="#FFFFFF")
    title_label.pack(pady=10)

    # Status label with dynamic text that changes as scanning progresses
    status_label = ctk.CTkLabel(tab, text="Status: Idle", font=("Roboto", 14), fg="#FF4500")
    status_label.pack(pady=5)

    # Input field and buttons with padding for better layout
    ctk.CTkLabel(tab, text="Target IP or Domain", font=("Roboto", 14)).pack(pady=5)
    scanner_target_entry = ctk.CTkEntry(tab, width=500, font=("Roboto", 14))
    scanner_target_entry.pack(pady=5)

    # Action buttons with green background and hover effects
    ctk.CTkButton(tab, text="Start Port Scan", command=lambda: threading.Thread(target=run_port_scan).start(),
                  font=("Roboto", 14), fg_color="#28A745", hover_color="#218838").pack(pady=5)
    ctk.CTkButton(tab, text="Start Dir Scan", command=lambda: threading.Thread(target=run_dir_scan).start(),
                  font=("Roboto", 14), fg_color="#28A745", hover_color="#218838").pack(pady=5)

    # Output textbox with a nice border and scrollable feature
    scanner_output = ctk.CTkTextbox(tab, height=400, width=800, font=("Roboto", 12), wrap="word")
    scanner_output.pack(pady=10)

    # Optional scrollbar for better UX if the output exceeds the visible area
    scrollbar = ctk.CTkScrollbar(tab, command=scanner_output.yview)
    scrollbar.pack(side="right", fill="y")
    scanner_output.configure(yscrollcommand=scrollbar.set)

    # Adding custom tags to apply color coding to the output
    scanner_output.tag_configure("green", foreground="#28A745")
    scanner_output.tag_configure("red", foreground="#FF0000")
    scanner_output.tag_configure("yellow", foreground="#FFFF00")
