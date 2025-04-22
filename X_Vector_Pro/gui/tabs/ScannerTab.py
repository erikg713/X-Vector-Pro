# gui/tabs/scanner_tab.py

import customtkinter as ctk
import threading
from core.scanner import run_scan  # Hook to scanning logic
from utils.logger import log

class ScannerTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.port_range_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()
ctk.CTkLabel(scanner_tab, text="Target IP or Domain").pack(pady=5)
scanner_target_entry = ctk.CTkEntry(scanner_tab, width=500)
scanner_target_entry.pack()

ctk.CTkButton(scanner_tab, text="Start Port Scan", command=lambda: threading.Thread(target=run_port_scan).start()).pack(pady=10)

scanner_output = ctk.CTkTextbox(scanner_tab, height=400, width=800)
scanner_output.pack()
    def build_ui(self):
        ctk.CTkLabel(self, text="Port Scanning", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Target IP/domain...")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.port_range_entry = ctk.CTkEntry(input_frame, textvariable=self.port_range_var, placeholder_text="Port range (e.g., 1-65535)")
        self.port_range_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.run_button = ctk.CTkButton(input_frame, text="Start Scan", command=self.run_scan_threaded)
        self.run_button.pack(side="left")

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Scan results will appear here...\n")
        self.output_box.configure(state="disabled")

    def run_scan_threaded(self):
        target = self.target_var.get().strip()
        port_range = self.port_range_var.get().strip()

        if not target or not port_range:
            self.show_status("Fill in all fields.")
            return

        threading.Thread(target=self.run_scan, args=(target, port_range), daemon=True).start()

    def run_scan(self, target, port_range):
        self.show_status(f"Running scan on {target}...")
        self.set_button_state(False)

        self.append_output(f"[INFO] Starting scan on {target}...\n")
        try:
            results = run_scan(target, port_range, gui_callback=self.append_output)
            self.append_output(f"[INFO] Scan completed.\n")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")

    def append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)

    def set_button_state(self, state: bool):
        self.run_button.configure(state="normal" if state else "disabled")
