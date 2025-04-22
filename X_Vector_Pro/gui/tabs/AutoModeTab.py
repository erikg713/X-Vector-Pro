# gui/tabs/auto_mode_tab.py

import customtkinter as ctk
import threading
from core.auto_chain import run_auto_chain  # You’ll hook this to the full chain logic
from utils.logger import log

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

    def run_chain_threaded(self):
        target = self.target_var.get().strip()
        if not target:
            self.show_status("Enter a valid target.")
            return
        threading.Thread(target=self.run_chain, args=(target,), daemon=True).start()

    def run_chain(self, target):
        self.show_status(f"Running auto recon chain on {target}...")
        self.set_button_state(False)

        self.append_output(f"[AUTO] Starting full chain on {target}\n")
        try:
            results = run_auto_chain(target, gui_callback=self.append_output)
            self.append_output(f"[AUTO] Completed successfully.\n")
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
