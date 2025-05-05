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

    logs_buttons = ctk.CTkFrame(tab)
    logs_buttons.pack(pady=10)

    ctk.CTkButton(logs_buttons, text="Save Logs", command=save_logs).pack(side="left", padx=10)
    ctk.CTkButton(logs_buttons, text="Clear Logs", command=clear_logs).pack(side="left", padx=10)
    ctk.CTkButton(logs_buttons, text="Export HTML", command=export_html_report).pack(side="left", padx=10)
