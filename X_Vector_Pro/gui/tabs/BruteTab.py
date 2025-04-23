# gui/tabs/brute_tab.py

import os
import threading
import customtkinter as ctk
from tkinter import filedialog
from core.brute_force import run_brute_force
from utils.toast import show_toast

# Define default module mappings
DEFAULT_PORTS = {
    "FTP": 21,
    "SSH": 22,
    "MySQL": 3306,
    "WordPress": 80
}

DEFAULT_WORDLISTS = {
    "FTP": "ftp_default_creds.txt",
    "SSH": "ssh_common.txt",
    "MySQL": "mysql_login.txt",
    "WordPress": "wp_login.txt"
}

class BruteTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.wordlist_path = ctk.StringVar()
        self.stealth_var = ctk.BooleanVar()
        self.module_var = ctk.StringVar()
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Brute Force Tool", font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Target
        ctk.CTkLabel(self, text="Target IP/Host:").pack()
        self.target_entry = ctk.CTkEntry(self)
        self.target_entry.pack(fill="x", padx=10, pady=5)

        # Module Dropdown
        ctk.CTkLabel(self, text="Module:").pack()
        self.module_dropdown = ctk.CTkOptionMenu(
            self, variable=self.module_var,
            values=list(DEFAULT_PORTS.keys()),
            command=self.auto_fill_port
        )
        self.module_dropdown.pack(fill="x", padx=10, pady=5)

        # Port
        ctk.CTkLabel(self, text="Port:").pack()
        self.port_entry = ctk.CTkEntry(self)
        self.port_entry.pack(fill="x", padx=10, pady=5)

        # Wordlist
        ctk.CTkLabel(self, text="Wordlist File:").pack()
        wordlist_frame = ctk.CTkFrame(self)
        wordlist_frame.pack(fill="x", padx=10, pady=5)
        self.wordlist_entry = ctk.CTkEntry(wordlist_frame, textvariable=self.wordlist_path)
        self.wordlist_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(wordlist_frame, text="Browse", command=self.browse_wordlist).pack(side="right")

        # Stealth mode
        ctk.CTkCheckBox(self, text="Enable Stealth Mode", variable=self.stealth_var).pack(pady=(0, 10))

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.set(0)

        # Run button
        self.run_button = ctk.CTkButton(self, text="Run Brute Force", command=self.run_brute)
        self.run_button.pack(pady=5)

        # Output box
        self.output_box = ctk.CTkTextbox(self, height=250)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10)

    def auto_fill_port(self, module_name):
        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, str(DEFAULT_PORTS.get(module_name, "")))
        self.wordlist_path.set(f"wordlists/{DEFAULT_WORDLISTS.get(module_name, '')}")

    def browse_wordlist(self):
        path = filedialog.askopenfilename(initialdir="wordlists/", title="Select Wordlist")
        if path:
            self.wordlist_path.set(path)

    def run_brute(self):
        module = self.module_var.get()
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        wordlist = self.wordlist_path.get().strip()
        stealth = self.stealth_var.get()

        if not all([module, target, port, wordlist]):
            self.output_log("[!] Please fill in all fields.")
            return

        try:
            port = int(port)
        except ValueError:
            self.output_log("[!] Invalid port.")
            return

        self.output_box.delete("1.0", "end")
        self.output_log(f"[*] Starting brute-force on {target}:{port} with {module}...")

        self.run_button.configure(state="disabled", text="Running...")
        self.progress.pack()
        self.progress.start()

        def logger(msg):
            self.output_log(msg)
            self.save_log(msg)

        def task():
            try:
                result = run_brute_force(
                    module_name=module,
                    target=target,
                    port=port,
                    wordlist_file=wordlist,
                    stealth_mode=stealth,
                    logger=logger
                )
                self.output_log(f"\n[=] Result: {result}")
                show_toast("Brute-force Complete", style=result.get("status", "info"))
            except Exception as e:
                self.output_log(f"[ERROR] {e}")
                show_toast("Brute-force Failed", style="error")
            finally:
                self.run_button.configure(state="normal", text="Run Brute Force")
                self.progress.stop()
                self.progress.pack_forget()

        threading.Thread(target=task, daemon=True).start()

    def output_log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def save_log(self, message):
        os.makedirs("logs", exist_ok=True)
        with open("logs/brute_log.txt", "a") as f:
            f.write(message + "\n")
