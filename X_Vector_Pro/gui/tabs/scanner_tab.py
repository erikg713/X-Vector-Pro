import customtkinter as ctk
import threading
from core.scanner import run_scan  # Your scanning logic from core/scanner.py

class ScannerTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.port_range_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()

    def build_ui(self):
        # Title
        ctk.CTkLabel(self, text="Port Scanner", font=("Segoe UI", 20, "bold")).pack(pady=(10, 5))

        # Input Frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Target IP / Domain")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.port_range_entry = ctk.CTkEntry(input_frame, textvariable=self.port_range_var, placeholder_text="Port range (e.g., 20-80)")
        self.port_range_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.scan_button = ctk.CTkButton(input_frame, text="Start Scan", command=self.start_scan_threaded)
        self.scan_button.pack(side="left")

        # Status Label
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        # Output Box
        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Scan results will appear here...\n")
        self.output_box.configure(state="disabled")

    def start_scan_threaded(self):
        target = self.target_var.get().strip()
        port_range = self.port_range_var.get().strip()

        if not target or not port_range:
            self.update_status("Please fill in all fields.")
            return

        threading.Thread(target=self.run_scan, args=(target, port_range), daemon=True).start()

    def run_scan(self, target, port_range):
        self.update_status(f"Scanning {target} on ports {port_range}...")
        self.toggle_scan_button(False)

        self.append_output(f"[INFO] Starting scan on {target} ports {port_range}\n")

        try:
            results = run_scan(target, port_range, gui_callback=self.append_output)
            self.append_output(f"\n[INFO] Scan finished.\n")
        except Exception as e:
            self.append_output(f"\n[ERROR] {str(e)}\n")
        finally:
            self.update_status("Idle")
            self.toggle_scan_button(True)

    def append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def update_status(self, message):
        self.status_var.set(message)

    def toggle_scan_button(self, enabled):
        state = "normal" if enabled else "disabled"
        self.scan_button.configure(state=state)
