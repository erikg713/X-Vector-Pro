# gui/tabs/ids_tab.py

import os
import json
import random
import threading
from tkinter import messagebox

import customtkinter as ctk
# For Tor support via PySocks
try:
    import socks
    import socket
except ImportError:
    socks = None

from core.ids import suricata_manager, auto_analyzer
from utils.logger import log
from gui.dashboard import show_toast  # your existing toast helper


class IDSTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.status_var     = ctk.StringVar(value="Idle")
        self.stealth_var    = ctk.BooleanVar(value=False)
        self.use_tor_var    = ctk.BooleanVar(value=False)
        self.use_proxy_var  = ctk.BooleanVar(value=False)
        self.last_alerts    = []
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Intrusion Detection System", font=("Segoe UI", 18, "bold"))\
            .pack(pady=(10, 5))

        # Stealth / Proxy options
        opts = ctk.CTkFrame(self)
        opts.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkCheckBox(opts, text="Stealth Mode",   variable=self.stealth_var).pack(side="left", padx=5)
        ctk.CTkCheckBox(opts, text="Use Tor",         variable=self.use_tor_var).pack(side="left", padx=5)
        ctk.CTkCheckBox(opts, text="Rotate Proxies", variable=self.use_proxy_var).pack(side="left", padx=5)

        # Start button
        self.start_button = ctk.CTkButton(self, text="Start IDS", command=self.start_ids_threaded)
        self.start_button.pack(pady=(0, 10))

        # Status
        ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI",12))\
            .pack(pady=(0, 10))

        # Alerts output
        self.alert_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.alert_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.alert_box.insert("end", "Alerts will appear here...\n")
        self.alert_box.configure(state="disabled")

    def start_ids_threaded(self):
        threading.Thread(target=self.run_ids, daemon=True).start()

    def run_ids(self):
        self.show_status("Initializing IDS...")
        self.set_button_state(False)
        try:
            self.apply_network_cloaking()

            if not suricata_manager.is_running():
                suricata_manager.start_suricata()
                log.info("Suricata started")

            self.append_alert("[INFO] Suricata running. Checking for threats...\n")
            alerts = auto_analyzer.check_for_threats()
            self.last_alerts = alerts

            for a in alerts:
                entry = f"[ALERT] {a['timestamp']} - {a['alert']}\n"
                if not self.stealth_var.get():
                    self.append_alert(entry)

            if self.stealth_var.get():
                self.encrypt_logs(alerts)
                show_toast(self.master, "Alerts securely logged (stealth mode)")
                # hide visible logs
                self.alert_box.delete("1.0", "end")
            else:
                show_toast(self.master, f"IDS check complete: {len(alerts)} alerts")

        except Exception as e:
            log.error(f"IDS error: {e}")
            self.append_alert(f"[ERROR] {e}\n")
            show_toast(self.master, f"IDS error: {e}")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")

    def apply_network_cloaking(self):
        # Tor
        if self.use_tor_var.get():
            if socks:
                try:
                    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
                    socket.socket = socks.socksocket
                    log.info("Tor proxy applied")
                except Exception as e:
                    log.error(f"Tor setup failed: {e}")
                    show_toast(self.master, "Tor setup failed")
            else:
                log.warning("PySocks not installed")
                show_toast(self.master, "Install PySocks for Tor support")

        # Proxy rotation
        if self.use_proxy_var.get():
            try:
                with open("proxies.txt") as f:
                    proxies = [p.strip() for p in f if p.strip()]
                if not proxies:
                    raise ValueError("Proxy list empty")
                proxy = random.choice(proxies)
                os.environ["HTTP_PROXY"]  = proxy
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

    def show_status(self, text):
        self.status_var.set(text)

    def set_button_state(self, enabled: bool):
        self.start_button.configure(state="normal" if enabled else "disabled")
