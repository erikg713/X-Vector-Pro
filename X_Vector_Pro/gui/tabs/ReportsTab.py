import os
import json
import threading
import requests
import threads
import customtkinter as ctk
from core.reports import report_manager
from utils.logger import log
from gui.dashboard import show_toast
from tkinter import ttk
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from core.report import generate_report  # core should return a report string or file path

class ReportTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.generate_button = QPushButton("Generate Report")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.generate_button)
        layout.addWidget(self.output)
        self.setLayout(layout)

        self.generate_button.clicked.connect(self.handle_generate)

    def handle_generate(self):
        self.output.setText("Generating report...")
        try:
            report = generate_report()
            self.output.setText(report)
        except Exception as e:
            self.output.setText(f"Error: {str(e)}")
class ReportsTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.status_var = ctk.StringVar(value="Idle")
        self.stealth_var = ctk.BooleanVar(value=False)
        self.use_tor_var = ctk.BooleanVar(value=False)
        self.use_proxy_var = ctk.BooleanVar(value=False)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Reports", font=("Segoe UI", 18, "bold"))\
            .pack(pady=(10, 5))

        # Stealth / Proxy options
        opts = ctk.CTkFrame(self)
        opts.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkCheckBox(opts, text="Stealth Mode", variable=self.stealth_var).pack(side="left", padx=5)
        ctk.CTkCheckBox(opts, text="Use Tor", variable=self.use_tor_var).pack(side="left", padx=5)
        ctk.CTkCheckBox(opts, text="Rotate Proxies", variable=self.use_proxy_var).pack(side="left", padx=5)

        # Start button
        self.start_button = ctk.CTkButton(self, text="Generate Reports", command=self.start_report_threaded)
        self.start_button.pack(pady=(0, 10))

        # Status
        ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))\
            .pack(pady=(0, 10))

        # Report output (Invisible in stealth mode)
        self.report_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.report_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.report_box.insert("end", "Reports will appear here...\n")
        self.report_box.configure(state="disabled")

        # Progress Spinner (Invisible operation tweak)
        self.spinner = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.spinner.pack(padx=20, pady=10)
        self.spinner.place_forget()  # Hide by default

    def start_report_threaded(self):
        threading.Thread(target=self.run_report, daemon=True).start()

    def run_report(self):
        self.show_status("Generating Report...")
        self.set_button_state(False)
        try:
            self.apply_network_cloaking()

            reports = report_manager.generate_reports()
            for report in reports:
                if self.stealth_var.get():
                    self.encrypt_logs(report)
                else:
                    self.append_report(f"{report}\n")

            show_toast(self.master, "Report generation completed.")

        except Exception as e:
            log.error(f"Report error: {e}")
            self.append_report(f"[ERROR] {e}\n")
            show_toast(self.master, f"Report error: {e}")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")
            self.show_spinner(False)  # Hide the spinner

    def apply_network_cloaking(self):
        # Apply Tor and Proxy cloaking (same as other tabs)
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

        if self.use_proxy_var.get():
            try:
                with open("proxies.txt") as f:
                    proxies = [p.strip() for p in f if p.strip()]
                if not proxies:
                    raise ValueError("Proxy list empty")
                proxy = random.choice(proxies)
                os.environ["HTTP_PROXY"] = proxy
                os.environ["HTTPS_PROXY"] = proxy
                log.info(f"Rotated proxy: {proxy}")
            except Exception as e:
                log.error(f"Proxy rotation failed: {e}")
                show_toast(self.master, "Proxy rotation failed")

    def encrypt_logs(self, report):
        try:
            from utils.logger import encrypt_log
            payload = json.dumps({"report": report})
            encrypt_log(payload, f"{report}_result.enc")
            log.info(f"Encrypted report to {report}_result.enc")
        except Exception as e:
            log.error(f"Log encryption failed: {e}")
            show_toast(self.master, "Log encryption failed")

    def append_report(self, text):
        self.report_box.configure(state="normal")
        self.report_box.insert("end", text)
        self.report_box.see("end")
        self.report_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)

    def set_button_state(self, enabled: bool):
        self.start_button.configure(state="normal" if enabled else "disabled")

    def show_spinner(self, show: bool):
        if show:
            self.spinner.place(x=100, y=320)  # Position it appropriately
            self.spinner.start()
        else:
            self.spinner.place_forget()  # Hide the spinner
            self.spinner.stop()# engine/scanner.py
import requests

PLUGIN_PATHS = [
    "/wp-content/plugins/", "/wp-content/themes/",
]

HEADERS = {"User-Agent": "X-VectorScanner/1.0"}

def check_plugin_paths(url):
    results = {}
    for path in PLUGIN_PATHS:
        full_url = url.rstrip("/") + path
        try:
            r = requests.get(full_url, headers=HEADERS, timeout=5)
            results[path] = r.status_code
        except requests.RequestException:
            results[path] = "Error"
    return results# engine/scanner.py
