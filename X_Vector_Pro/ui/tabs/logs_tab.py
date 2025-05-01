import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

LOGS_DIR = "logs"
DEFAULT_LOG_FILE = os.path.join(LOGS_DIR, "xvector.log")

class LogsTab:
    def __init__(self, parent, toast_manager):
        self.toast = toast_manager
        self.frame = ttk.Frame(parent)

        self.log_content = tk.StringVar()
        self.selected_log = tk.StringVar()

        self._build_ui()
        self._load_logs()

    def _build_ui(self):
        ttk.Label(self.frame, text="Log Viewer", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Top bar: dropdown + buttons
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(pady=5)

        ttk.Label(top_frame, text="Select Log:").pack(side="left", padx=5)
        self.dropdown = ttk.OptionMenu(top_frame, self.selected_log, "", command=self._display_log)
        self.dropdown.pack(side="left", padx=5)

        ttk.Button(top_frame, text="Refresh Logs", command=self._refresh_logs).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Clear Current Log", command=self._clear_log).pack(side="left", padx=5)

        # Text area
        self.text_box = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=90, height=25)
        self.text_box.pack(pady=10)

    def _load_logs(self):
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

        self.logs = [f for f in os.listdir(LOGS_DIR) if f.endswith(".log") or f.endswith(".txt")]
        if not self.logs:
            # If no logs exist, create a default
            with open(DEFAULT_LOG_FILE, "w") as f:
                f.write(f"[{datetime.now()}] X-Vector Pro started.\n")
            self.logs.append("xvector.log")

        self.selected_log.set(self.logs[0])
        self._update_dropdown()
        self._display_log(self.logs[0])

    def _update_dropdown(self):
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for log_file in self.logs:
            menu.add_command(label=log_file, command=lambda f=log_file: self._display_log(f))

    def _display_log(self, filename):
        path = os.path.join(LOGS_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, content)
        except Exception as e:
            self.toast.show(f"Failed to load log: {e}")

    def _refresh_logs(self):
        self._load_logs()
        self.toast.show("Logs refreshed.")

    def _clear_log(self):
        path = os.path.join(LOGS_DIR, self.selected_log.get())
        if os.path.exists(path):
            try:
                with open(path, "w") as f:
                    f.write(f"[{datetime.now()}] Log cleared.\n")
                self._display_log(self.selected_log.get())
                self.toast.show("Log cleared.")
            except Exception as e:
                self.toast.show(f"Error clearing log: {e}")




import customtkinter as ctk
from tkinter import messagebox
from utils.logger import log_to_central

def load_logs_tab(tab):
    global logs_output
    logs_output = ctk.CTkTextbox(tab, height=450, width=800)
    logs_output.pack(pady=10)

    def export_html_report():
        try:
            html = logs_output.get("1.0", "end")
            formatted = "<br>".join(html.splitlines())
            with open("xvector_report.html", "w") as f:
                f.write(f"<html><body><h2>X-Vector Pro Report</h2><pre>{formatted}</pre></body></html>")
            log_to_central("[+] Exported HTML report: xvector_report.html", logs_output)
        except Exception as e:
            log_to_central(f"[!] Report export failed: {e}", logs_output)

    def save_logs():
        try:
            with open("xvector_log.txt", "w") as f:
                f.write(logs_output.get("1.0", "end"))
            log_to_central("[+] Logs saved to xvector_log.txt", logs_output)
        except Exception as e:
            log_to_central(f"[!] Error saving logs: {e}", logs_output)

    def clear_logs():
        logs_output.delete("0.0", "end")
        log_to_central("[+] Logs cleared", logs_output)

    logs_buttons = ctk.CTkFrame(tab)
    logs_buttons.pack(pady=10)

    ctk.CTkButton(logs_buttons, text="Save Logs", command=save_logs).pack(side="left", padx=10)
    ctk.CTkButton(logs_buttons, text="Clear Logs", command=clear_logs).pack(side="left", padx=10)
    ctk.CTkButton(logs_buttons, text="Export HTML", command=export_html_report).pack(side="left", padx=10)
