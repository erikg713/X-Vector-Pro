import customtkinter as ctk
import threading
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter.messagebox as msgbox
from utils.recon_utils import perform_whois, perform_dns_lookup, perform_ip_geolocation

class ReconTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.running = False  # Flag to track if recon is running
        self.recon_log_file = "recon_log.txt"  # Log file path
        self.email_log = "recipient@example.com"  # Email recipient for reports
        self._setup_ui()

    def _setup_ui(self):
        """Sets up all UI elements for the Recon Tab."""
        header_frame = ctk.CTkFrame(self, height=50, corner_radius=10, bg_color="#007BFF")
        header_frame.pack(fill="x", pady=(10, 5))

        title_label = ctk.CTkLabel(header_frame, text="Recon Viewer", font=("Roboto", 20, "bold"), fg="#FFFFFF")
        title_label.pack(pady=10)

        self.recon_view = ReconViewer(self)
        self.recon_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh_recon, font=("Roboto", 14), fg_color="#28A745", hover_color="#218838")
        self.refresh_button.pack(pady=15)

        self.refresh_button.bind("<Enter>", lambda e: self.show_tooltip("Refresh Recon Data"))
        self.refresh_button.bind("<Leave>", lambda e: self.hide_tooltip())

        self.tooltip_label = ctk.CTkLabel(self, text="", font=("Roboto", 10), fg="#FFFFFF", bg_color="#007BFF")
        self.tooltip_label.pack_forget()

        self.loading_spinner = ctk.CTkProgressBar(self, mode="indeterminate", width=200, height=5)
        self.loading_spinner.pack(pady=10)
        self.loading_spinner.set(0)
        self.loading_spinner.grid_forget()

        # Recon process setup
        ctk.CTkLabel(self, text="Enter Target Domain or IP", font=("Segoe UI", 12)).pack(pady=(10, 4))
        self.target_entry = ctk.CTkEntry(self, width=300)
        self.target_entry.pack(pady=(5, 20))

        self.start_button = ctk.CTkButton(self, text="Start Recon", command=self.start_recon, width=180)
        self.start_button.pack(pady=(10, 20))

        self.stop_button = ctk.CTkButton(self, text="Stop Recon", command=self.stop_recon, width=180, state="disabled")
        self.stop_button.pack(pady=(10, 20))

        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.pack(pady=(10, 20))

        self.log_text = ctk.CTkTextbox(self, width=500, height=200, state="disabled")
        self.log_text.pack(pady=(10, 20))

        self.recon_type = ctk.CTkOptionMenu(self, values=["WHOIS", "DNS Lookup", "IP Geolocation"], width=200)
        self.recon_type.set("WHOIS")
        self.recon_type.pack(pady=(5, 20))

    def log(self, message):
        """Logs messages to both the log textbox and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        self.log_text.config(state="normal")
        self.log_text.insert("end", log_message + "\n")
        self.log_text.config(state="disabled")
        
        with open(self.recon_log_file, "a") as log_file:
            log_file.write(log_message + "\n")
        
        self.log_text.yview("end")

    def send_email_log(self, subject, body):
        """Send the recon log as an email after recon completion."""
        try:
            msg = MIMEMultipart()
            msg['From'] = 'your_email@example.com'
            msg['To'] = self.email_log
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Email server setup
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()

            self.log(f"Log sent to email: {self.email_log}")
        except Exception as e:
            self.log(f"Error sending email: {str(e)}")

    def start_recon(self):
        """Starts the Recon process."""
        if self.running:
            msgbox.showinfo("Already Running", "Recon process is already in progress.")
            return

        target = self.target_entry.get().strip()
        if not target:
            msgbox.showwarning("Input Error", "Please enter a valid target domain or IP.")
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("Recon process started.")
        
        threading.Thread(target=self.run_recon, args=(target,)).start()

    def stop_recon(self):
        """Stops the Recon process."""
        if not self.running:
            msgbox.showinfo("Not Running", "Recon is not currently running.")
            return

        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("Recon process stopped.")

    def run_recon(self, target):
        """Handles the execution of the Recon process."""
        try:
            recon_type = self.recon_type.get()
            if recon_type == "WHOIS":
                self.log("Starting WHOIS Lookup...")
                self.progress_bar.set(0.2)
                perform_whois(self, target)
            elif recon_type == "DNS Lookup":
                self.log("Starting DNS Lookup...")
                self.progress_bar.set(0.4)
                perform_dns_lookup(self, target)
            elif recon_type == "IP Geolocation":
                self.log("Starting IP Geolocation Lookup...")
                self.progress_bar.set(0.6)
                perform_ip_geolocation(self, target)

            self.progress_bar.set(1.0)
            self.log(f"{recon_type} Lookup completed successfully.")
            
            # Send log email
            email_subject = f"{recon_type} Recon Log"
            with open(self.recon_log_file, "r") as log_file:
                log_content = log_file.read()
            self.send_email_log(email_subject, log_content)

            msgbox.showinfo("Recon Completed", f"{recon_type} Recon completed successfully.")
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            self.log(error_message)
            msgbox.showerror("Error", error_message)
        finally:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.progress_bar.set(0.0)

import customtkinter as ctk import threading import subprocess import time

class ReconTab(ctk.CTkFrame): def init(self, parent, **kwargs): super().init(parent, **kwargs) self.running = False self.log_file = "recon_log.txt" self._initialize_ui()

def _initialize_ui(self):
    ctk.CTkLabel(self, text="Recon - Information Gathering", font=("Segoe UI", 14)).pack(pady=(10, 4))
    ctk.CTkLabel(self, text="Start reconnaissance by entering a target and pressing 'Start Recon'.", font=("Segoe UI", 12)).pack(pady=(10, 4))
    ctk.CTkLabel(self, text="Target Domain or IP:", font=("Segoe UI", 12)).pack(pady=(10, 4))

    self.target_entry = ctk.CTkEntry(self, width=300)
    self.target_entry.pack(pady=(5, 15))

    self.start_button = ctk.CTkButton(self, text="Start Recon", command=self._start_recon, width=180)
    self.start_button.pack(pady=(10, 10))

    self.stop_button = ctk.CTkButton(self, text="Stop Recon", command=self._stop_recon, width=180, state="disabled")
    self.stop_button.pack(pady=(10, 10))

    self.progress_bar = ctk.CTkProgressBar(self, width=500)
    self.progress_bar.set(0)
    self.progress_bar.pack(pady=(20, 15))

    self.output_box = ctk.CTkTextbox(self, height=200, width=600)
    self.output_box.pack(pady=(10, 15))

def _start_recon(self):
    target = self.target_entry.get().strip()
    if not target:
        self._log_output("[!] Please enter a valid target domain or IP.\n")
        return

    self._log_output(f"[*] Initiating reconnaissance on: {target}\n")
    self.running = True
    self.start_button.configure(state="disabled")
    self.stop_button.configure(state="normal")
    self.progress_bar.set(0)

    threading.Thread(target=self._run_recon_process, args=(target,), daemon=True).start()

def _run_recon_process(self, target):
    tasks = [self._nmap_scan, self._whois_lookup]
    total_tasks = len(tasks)

    for idx, task in enumerate(tasks, start=1):
        if not self.running:
            self._log_output("[-] Reconnaissance interrupted by user.\n")
            break

        self._log_output(f"[*] Starting task {idx}/{total_tasks}: {task.__name__}\n")
        task(target)
        self.progress_bar.set(idx / total_tasks)

    if self.running:
        self._log_output("[+] Reconnaissance completed successfully.\n")

    self._finalize_recon()

def _nmap_scan(self, target):
    try:
        self._log_output(f"[*] Running nmap scan on {target}...\n")
        result = subprocess.run(["nmap", "-Pn", target], capture_output=True, text=True, timeout=120)
        self._log_output(result.stdout)
        self._append_log(result.stdout)
    except Exception as e:
        self._log_output(f"[!] Nmap scan error: {e}\n")

def _whois_lookup(self, target):
    try:
        self._log_output(f"[*] Performing whois lookup on {target}...\n")
        result = subprocess.run(["whois", target], capture_output=True, text=True, timeout=60)
        self._log_output(result.stdout)
        self._append_log(result.stdout)
    except Exception as e:
        self._log_output(f"[!] Whois lookup error: {e}\n")

def _stop_recon(self):
    self.running = False

def _finalize_recon(self):
    self.running = False
    self.start_button.configure(state="normal")
    self.stop_button.configure(state="disabled")
    self.progress_bar.set(0)

def _log_output(self, message):
    self.output_box.insert("end", message)
    self.output_box.see("end")

def _append_log(self, content):
    with open(self.log_file, "a") as file:
        file.write(content + "\n")

