# gui/tabs/ids_tab.py

import customtkinter as ctk
import threading
from core.ids import suricata_manager, auto_analyzer  # Hook to IDS logic
from utils.logger import log

class IDSTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Intrusion Detection", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        self.start_button = ctk.CTkButton(self, text="Start IDS", command=self.start_ids)
        self.start_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        self.alert_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.alert_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.alert_box.insert("end", "Alerts will appear here...\n")
        self.alert_box.configure(state="disabled")

    def start_ids(self):
        threading.Thread(target=self.run_ids_threaded, daemon=True).start()

    def run_ids_threaded(self):
        self.show_status("Starting IDS...")
        if not suricata_manager.is_running():
            suricata_manager.start_suricata()

        self.append_alert(f"[INFO] Suricata started. Checking for threats...\n")
        alerts = auto_analyzer.check_for_threats()

        for alert in alerts:
            self.append_alert(f"[ALERT] {alert['timestamp']} - {alert['alert']}\n")

        self.show_status("Idle")

    def append_alert(self, alert_text):
        self.alert_box.configure(state="normal")
        self.alert_box.insert("end", alert_text)
        self.alert_box.see("end")
        self.alert_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)
