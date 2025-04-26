# gui/tabs/ids_tab.py

import os
import json
import random
import threading
import time
from tkinter import messagebox

import customtkinter as ctk
from tkinter import ttk

# Tor support
try:
    import socks
    import socket
except ImportError:
    socks = None

from core.ids import suricata_manager, auto_analyzer
from utils.logger import log
from gui.dashboard import show_toast


class IDSTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.status_var = ctk.StringVar(value="Idle")
        self.stealth_var = ctk.BooleanVar(value=False)
        self.use_tor_var = ctk.BooleanVar(value=False)
        self.use_proxy_var = ctk.BooleanVar(value=False)
        self.last_alerts = []
        self.running = False
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Intrusion Detection System", font=("Segoe UI", 18, "bold"))\
            .pack(pady=(10, 5))

        # Options
        opts = ctk.CTkFrame(self)
        opts.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkCheckBox(opts, text="Stealth Mode", variable=self.stealth_var).pack(side="left", padx=5)
        ctk.CTkCheckBox(opts, text="Use Tor", variable=self.use_tor_var).pack(side="left", padx=5)
        ctk.CTkCheckBox(opts, text="Rotate Proxies", variable=self.use_proxy_var).pack(side="left", padx=5)

        # Buttons
        btns = ctk.CTkFrame(self)
        btns.pack(pady=(0, 10))
        self.start_button = ctk.CTkButton(btns, text="Start IDS", command=self.start_ids_threaded)
        self.start_button.pack(side="left", padx=5)
        self.stop_button = ctk.CTkButton(btns, text="Stop IDS", command=self.stop_ids, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        # Status
        ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))\
            .pack(pady=(0, 10))

        # Alert box
        self.alert_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.alert_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.alert_box.insert("end", "Alerts will appear here...\n")
        self.alert_box.configure(state="disabled")

        # Progress spinner
        self.spinner = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.spinner.pack(padx=20, pady=10)
        self.spinner.place_forget()

    def start_ids_threaded(self):
        if not self.running:
            threading.Thread(target=self.run_ids_loop, daemon=True).start()

    def run_ids_loop(self):
        self.running = True
        self.show_status("IDS Running...")
        self.toggle_buttons(start=False)
        self.show_spinner(True)
        self.apply_network_cloaking()

        try:
            if not suricata_manager.is_running():
                suricata_manager.start_suricata()
                log.info("Suricata started")

            show_toast(self.master, "Suricata running. Monitoring network...")

            while self.running:
                alerts = auto_analyzer.check_for_threats()
                if alerts:
                    self.last_alerts.extend(alerts)
                    for a in alerts:
                        entry = f"[ALERT] {a['timestamp']} - {a['alert']}\n"
                        if not self.stealth_var.get():
                            self.append_alert(entry)

                    if self.stealth_var.get():
                        self.encrypt_logs(self.last_alerts)
                        self.clear_alert_box()
                        show_toast(self.master, "Stealth mode: alerts encrypted.")
                time.sleep(10)  # Adjustable polling interval

        except Exception as e:
            log.error(f"IDS loop error: {e}")
            show_toast(self.master, f"IDS Error: {e}")
        finally:
            self.running = False
            self.show_status("Idle")
            self.toggle_buttons(start=True)
            self.show_spinner(False)

    def stop_ids(self):
        self.running = False
        show_toast(self.master, "IDS stopped.")

    def apply_network_cloaking(self):
        # Tor
        if self.use_tor_var.get() and socks:
            try:
                socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket
                log.info("Tor proxy applied")
            except Exception as e:
                log.error(f"Tor setup failed: {e}")
                show_toast(self.master, "Tor setup failed")
        elif self.use_tor_var.get() and not socks:
            show_toast(self.master, "Install PySocks for Tor support")

        # Proxy rotation
        if self.use_proxy_var.get():
            try:
                with open("proxies.txt") as f:
                    proxies = [p.strip() for p in f if p.strip()]
                if proxies:
                    proxy = random.choice(proxies)
                    os.environ["HTTP_PROXY"] = proxy
                    os.environ["HTTPS_PROXY"] = proxy
                    log.info(f"Rotated proxy: {proxy}")
            except Exception as e:
                log.error(f"Proxy rotation failed: {e}")
                show_toast(self.master, "Proxy rotation failed")

    def encrypt_logs(self, alerts):
        try:
            from utils.logger import encrypt_log
            payload = json.dumps(alerts)
            encrypt_log(payload, "ids_alerts.enc")
            log.info("Encrypted IDS alerts to ids_alerts.enc")
        except Exception as e:
            log.error(f"Log encryption failed: {e}")
            show_toast(self.master, "Log encryption failed")

    def append_alert(self, text):
        self.alert_box.configure(state="normal")
        self.alert_box.insert("end", text)
        self.alert_box.see("end")
        self.alert_box.configure(state="disabled")

    def clear_alert_box(self):
        self.alert_box.configure(state="normal")
        self.alert_box.delete("1.0", "end")
        self.alert_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)

    def toggle_buttons(self, start=True):
        self.start_button.configure(state="normal" if start else "disabled")
        self.stop_button.configure(state="disabled" if start else "normal")

    def show_spinner(self, show=True):
        if show:
            self.spinner.place(x=100, y=320)
            self.spinner.start()
        else:
            self.spinner.stop()
            self.spinner.place_forget()
