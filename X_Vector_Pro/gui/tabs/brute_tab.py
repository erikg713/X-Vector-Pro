# gui/tabs/brute_tab.py

import os
import threading
import datetime
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
        self.is_running = False
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
        self.progress.pack(fill="x", padx=10, pady=5)

        # Buttons
        self.run_button = ctk.CTkButton(self, text="Run Brute Force", command=self.run_brute)
        self.run_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_brute, state="disabled")
        self.stop_button.pack(pady=5)

        # Output
        self.output_box = ctk.CTkTextbox(self, height=250)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10)

    def auto_fill_port(self, module_name):
        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, str(DEFAULT_PORTS.get(module_name, "")))
        self.wordlist_path.set(f"wordlists/{DEFAULT_WORDLISTS.get(module_name, '')}")

    def browse_wordlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.wordlist_path.set(file_path)

    def log_output(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_box.insert("end", f"[{timestamp}] {message}\n")
        self.output_box.see("end")

    def run_brute(self):
        if self.is_running:
            self.log_output("Brute force is already running.")
            return

        self.is_running = True
        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress.start()
        self.output_box.delete("1.0", "end")

        def task():
            try:
                target = self.target_entry.get()
                port = int(self.port_entry.get())
                wordlist = self.wordlist_path.get()
                module = self.module_var.get()
                stealth = self.stealth_var.get()

                self.log_output(f"Starting brute force on {target}:{port} using {wordlist} (stealth={stealth})")

                run_brute_force(
                    target=target,
                    port=port,
                    module=module,
                    wordlist_path=wordlist,
                    stealth=stealth,
                    output_callback=self.log_output,
                    stop_flag=lambda: not self.is_running
                )

                self.log_output("Brute force completed.")

            except Exception as e:
                self.log_output(f"Error: {str(e)}")
            finally:
                self.is_running = False
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.progress.stop()

        threading.Thread(target=task, daemon=True).start()

    def stop_brute(self):
        if self.is_running:
            self.is_running = False
            self.log_output("Brute force stopped by user.")
        else:
            self.log_output("No brute force process is running.")
