# gui/tabs/recon_tab.py
import threading
import customtkinter as ctk
from core.recon.recon_engine import run_recon  # Your recon logic
from utils.logger import log  # Logger

class ReconTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Reconnaissance", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Target IP/domain...")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.run_button = ctk.CTkButton(input_frame, text="Run Recon", command=self.run_recon_threaded)
        self.run_button.pack(side="left", padx=(5, 0))

        self.subdomain_button = ctk.CTkButton(input_frame, text="Scan Subdomains", command=self.run_subdomain_scan_threaded)
        self.subdomain_button.pack(side="left", padx=(5, 0))

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Recon results will appear here...\n")
        self.output_box.configure(state="disabled")

    def run_recon_threaded(self):
        target = self.target_var.get().strip()
        if not target:
            self.show_status("Enter a valid target.")
            return
        threading.Thread(target=self.run_recon, args=(target,), daemon=True).start()

    def run_recon(self, target):
        self.show_status(f"Running reconnaissance on {target}...")
        self.set_button_state(False)

        self.append_output(f"[INFO] Starting recon on {target}\n")
        try:
            results = run_recon(target, gui_callback=self.append_output)
            self.append_output(f"[INFO] Recon complete.\n")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")

    def run_subdomain_scan_threaded(self):
        target = self.target_var.get().strip()
        if not target:
            self.show_status("Enter a valid target.")
            return
        threading.Thread(target=self.subdomain_scan, args=(target,), daemon=True).start()

    def subdomain_scan(self, target):
        self.show_status(f"Scanning subdomains for {target}...")
        self.set_button_state(False)

        try:
            # Placeholder for actual subdomain scanning logic
            self.append_output(f"[INFO] Scanning subdomains for {target}...\n")
            self.append_output("[INFO] Found subdomain: test1.example.com\n")
            self.append_output("[INFO] Found subdomain: test2.example.com\n")
            self.append_output(f"[INFO] Subdomain scan complete.\n")
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
        self.subdomain_button.configure(state="normal" if state else "disabled")
