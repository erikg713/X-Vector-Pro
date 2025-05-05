import customtkinter as ctk
import threading
import smtplib
from datetime import datetime
from tkinter import filedialog, messagebox
from utils.scanner_utils import perform_port_scan, perform_vuln_scan
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class ScannerTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.targets = []
        self.configure_ui()

    def configure_ui(self):
        """Configure the ScannerTab UI elements."""
        self.label = ctk.CTkLabel(self, text="Enter target(s) separated by commas:")
        self.label.pack(pady=(10, 0))

        self.entry = ctk.CTkEntry(self, placeholder_text="e.g., 192.168.1.1, example.com", width=400)
        self.entry.pack(pady=(0, 10))

        self.add_button = ctk.CTkButton(self, text="Add Targets", command=self.add_targets)
        self.add_button.pack(pady=(0, 10))

        self.target_box = ctk.CTkTextbox(self, height=100, width=400)
        self.target_box.pack(pady=(0, 10))

        self.scan_button = ctk.CTkButton(self, text="Start Scan", command=self.start_scan)
        self.scan_button.pack(pady=(0, 10))

        self.save_button = ctk.CTkButton(self, text="Save Results", command=self.save_results)
        self.save_button.pack(pady=(0, 10))

        self.result_box = ctk.CTkTextbox(self, height=200, width=600)
        self.result_box.pack(pady=(0, 10))

        self.send_email_button = ctk.CTkButton(self, text="Send Results via Email", command=self.send_email_log)
        self.send_email_button.pack(pady=(0, 10))

    def update_result_box(self, message):
        """Append text to the result box and auto-scroll to the end."""
        self.result_box.insert("end", message + "\n")
        self.result_box.see("end")

    def add_targets(self):
        """Add targets from the entry box to the target list."""
        input_text = self.entry.get()
        targets = [t.strip() for t in input_text.split(',') if t.strip()]
        self.targets.extend(targets)
        self.target_box.delete("1.0", "end")
        self.target_box.insert("end", "\n".join(self.targets))
        self.entry.delete(0, 'end')

    def start_scan(self):
        """Initiate the scanning process."""
        if not self.targets:
            self.update_result_box("[!] No targets specified.")
            return
        self.scan_button.configure(state="disabled")
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        """Run the scan for all targets."""
        self.result_box.delete("1.0", "end")
        for target in self.targets:
            self.update_result_box(f"[+] Scanning target: {target}")
            try:
                results = perform_port_scan(target)  # Example custom scanning function
                self.update_result_box(results)
            except Exception as e:
                self.update_result_box(f"[!] Error scanning {target}: {e}")
        self.scan_button.configure(state="normal")

    def save_results(self):
        """Save scan results to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            results = self.result_box.get("1.0", "end").strip()
            with open(file_path, "w") as f:
                f.write(results)
            self.update_result_box(f"[+] Results saved to {file_path}")

    def send_email_log(self):
        """Send scan results via email."""
        sender_email = os.getenv("EMAIL_USER")
        receiver_email = os.getenv("EMAIL_TO")
        password = os.getenv("EMAIL_PASS")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        if not sender_email or not receiver_email or not password:
            self.update_result_box("[!] Email credentials are not set in environment variables.")
            return

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "X-Vector Pro Scan Results"

        results = self.result_box.get("1.0", "end").strip()
        message.attach(MIMEText(results, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(message)
            self.update_result_box("[+] Email sent successfully.")
        except Exception as e:
            self.update_result_box(f"[!] Failed to send email: {e}")
