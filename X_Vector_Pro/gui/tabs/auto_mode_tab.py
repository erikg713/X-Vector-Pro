# gui/tabs/auto_mode_tab.py

import customtkinter as ctk
import threading
import re
from core.auto_chain import run_auto_chain  # Ensure this function is implemented
from utils.logger import log  # Optional logging, use inside try/except as needed

class AutoModeTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Automated Recon + Exploit Chain", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Enter target IP or domain...")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.run_button = ctk.CTkButton(input_frame, text="Run Full Auto Chain", command=self.run_chain_threaded)
        self.run_button.pack(side="left")

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Status logs will appear here...\n")
        self.output_box.configure(state="disabled")

        # Clear Output Button
        self.clear_button = ctk.CTkButton(self, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(pady=(5, 10))

        # Spinner (progress indicator)
        self.spinner = ctk.CTkProgressBar(self, mode="indeterminate")
        self.spinner.pack(pady=5)
        self.spinner.place_forget()  # Initially hide it

    def run_chain_threaded(self):
        target = self.target_var.get().strip()
        if not target or not self.is_valid_target(target):
            self.show_status("Enter a valid target.")
            return
        threading.Thread(target=self.run_chain, args=(target,), daemon=True).start()

    def run_chain(self, target):
        self.show_status(f"Running auto recon chain on {target}...")
        self.set_button_state(False)
        self.show_spinner(True)
        self.append_output(f"[AUTO] Starting full chain on {target}\n")
        try:
            results = run_auto_chain(target, gui_callback=self.append_output)
            self.append_output(f"[AUTO] Completed successfully.\n")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")
            self.show_spinner(False)

    def append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)

    def set_button_state(self, state: bool):
        self.run_button.configure(state="normal" if state else "disabled")

    def show_spinner(self, show: bool):
        if show:
            self.spinner.place(x=100, y=320)  # Position it appropriately
            self.spinner.start()
        else:
            self.spinner.place_forget()  # Hide the spinner
            self.spinner.stop()  # Stop spinner animation

    def clear_output(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def is_valid_target(self, target):
        """Check if the input target is a valid IP or domain."""
        # Simple regex for IP and domain validation
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$"
        return bool(re.match(ip_pattern, target)) or bool(re.match(domain_pattern, target))
