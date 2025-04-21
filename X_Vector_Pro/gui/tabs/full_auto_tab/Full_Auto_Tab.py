import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from gui.components.styles import apply_dark_theme
from core.recon.auto_recon import run_auto_recon  # <- Uses enhanced version

class FullAutoTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        apply_dark_theme(self)

        self.target_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Idle")
        self.stealth_mode = tk.BooleanVar()

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="Target IP or Domain:", style="TLabel").pack(pady=(10, 5))
        target_entry = ttk.Entry(self, textvariable=self.target_var, width=40)
        target_entry.pack(pady=5)

        ttk.Checkbutton(
            self,
            text="Stealth Mode (Low Noise)",
            variable=self.stealth_mode
        ).pack(pady=5)

        self.start_button = ttk.Button(
            self,
            text="Start Full Auto Recon",
            command=self.start_recon_thread
        )
        self.start_button.pack(pady=(10, 5))

        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            foreground="cyan"
        )
        self.status_label.pack(pady=(10, 5))

        self.output_text = tk.Text(self, height=18, width=90, bg="#121212", fg="#00ff7f")
        self.output_text.pack(padx=10, pady=10)
        self.output_text.insert(tk.END, "[*] Waiting to begin recon...\n")
        self.output_text.configure(state=tk.DISABLED)

    def log_output(self, text):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def start_recon_thread(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("Input Error", "Please enter a target IP or domain.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.status_var.set("Recon in progress...")
        self.log_output(f"[+] Starting recon on {target}...")

        thread = threading.Thread(target=self.run_recon, args=(target,))
        thread.start()

    def run_recon(self, target):
        try:
            stealth = self.stealth_mode.get()
            self.log_output("[*] Stealth mode: ON" if stealth else "[*] Stealth mode: OFF")
            run_auto_recon(
                target_ip=target,
                stealth=stealth,
                save_to_db=True,
                logger=self.log_output  # logger hook passed
            )
            self.log_output("[+] Recon complete and logged securely.")
        except Exception as e:
            self.log_output(f"[!] Recon error: {e}")
        finally:
            self.status_var.set("Idle")
            self.start_button.config(state=tk.NORMAL)
