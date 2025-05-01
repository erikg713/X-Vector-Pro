import customtkinter as ctk
import threading, socket, requests
from tkinter import messagebox
from queue import Queue
import time
import customtkinter as ctk
import threading
from datetime import datetime
from utils.scanner_utils import perform_port_scan, perform_vuln_scan  # These are placeholder functions
import tkinter.messagebox as msgbox
import customtkinter as ctk
import threading
from datetime import datetime
import nmap  # Import the python-nmap library
import tkinter.messagebox as msgbox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import customtkinter as ctk
from tkinter import filedialog
from core.scanner import scan_target


class ScannerTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.targets = []

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

    def add_targets(self):
        input_text = self.entry.get()
        targets = [t.strip() for t in input_text.split(',') if t.strip()]
        self.targets.extend(targets)
        self.target_box.delete("1.0", "end")
        self.target_box.insert("end", "\n".join(self.targets))
        self.entry.delete(0, 'end')

    def start_scan(self):
        if not self.targets:
            self.result_box.insert("end", "[!] No targets specified.\n")
            return
        self.scan_button.configure(state="disabled")
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        def append_text(text):
            self.result_box.insert("end", text)
            self.result_box.see("end")

        self.result_box.delete("1.0", "end")
        for target in self.targets:
            self.after(0, append_text, f"[+] Scanning target: {target}\n")
            try:
                results = scan_target(target)
                self.after(0, append_text, results + "\n")
            except Exception as e:
                self.after(0, append_text, f"[!] Error scanning {target}: {e}\n")
        self.after(0, lambda: self.scan_button.configure(state="normal"))

    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            results = self.result_box.get("1.0", "end").strip()
            with open(file_path, "w") as f:
                f.write(results)
            self.result_box.insert("end", f"[+] Results saved to {file_path}\n")

    def send_email_log(self):
        sender_email = os.getenv("EMAIL_USER")
        receiver_email = os.getenv("EMAIL_TO")
        password = os.getenv("EMAIL_PASS")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        if not sender_email or not receiver_email or not password:
            self.result_box.insert("end", "[!] Email credentials are not set in environment variables.\n")
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
            self.result_box.insert("end", "[+] Email sent successfully.\n")
        except Exception as e:
            self.result_box.insert("end", f"[!] Failed to send email: {e}\n")
class ScannerTab:
    def __init__(self, parent):
        self.parent = parent
        self.running = False  # Flag to track if scanning is running
        self.scan_log_file = "scan_log.txt"  # Log file path
        self.email_log = "recipient@example.com"  # Email recipient for reports
        self.nm = nmap.PortScanner()  # Initialize the Nmap scanner
        
        # Initialize the user interface (UI)
        self._setup_ui()

    def _setup_ui(self):
        """Sets up all UI elements for the Scanner Tab."""
        # Title Label
        ctk.CTkLabel(self.parent, text="Scanner - Network Scanning", font=("Segoe UI", 14)).pack(pady=(10, 4))

        # Instructions
        ctk.CTkLabel(self.parent, text="Click 'Start Scan' to perform scanning.", font=("Segoe UI", 12)).pack(pady=(10, 4))

        # Target Input
        ctk.CTkLabel(self.parent, text="Enter Target Domain or IP", font=("Segoe UI", 12)).pack(pady=(10, 4))
        self.target_entry = ctk.CTkEntry(self.parent, width=300)
        self.target_entry.pack(pady=(5, 20))

        # Start Button
        self.start_button = ctk.CTkButton(self.parent, text="Start Scan", command=self.start_scan, width=180)
        self.start_button.pack(pady=(10, 20))

        # Stop Button (Disabled initially)
        self.stop_button = ctk.CTkButton(self.parent, text="Stop Scan", command=self.stop_scan, width=180, state="disabled")
        self.stop_button.pack(pady=(10, 20))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.parent, width=500)
        self.progress_bar.pack(pady=(10, 20))

        # Log Display Area
        self.log_text = ctk.CTkTextbox(self.parent, width=500, height=200, state="disabled")
        self.log_text.pack(pady=(10, 20))

        # Scan Options
        self.scan_options_label = ctk.CTkLabel(self.parent, text="Select Scan Type", font=("Segoe UI", 12))
        self.scan_options_label.pack(pady=(10, 4))

        self.scan_type = ctk.CTkOptionMenu(self.parent, values=["Port Scan", "Service Scan", "OS Scan"], width=200)
        self.scan_type.set("Port Scan")  # Default setting
        self.scan_type.pack(pady=(5, 20))

    def log(self, message):
        """Logs messages to both the log textbox and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        # Update the log display area
        self.log_text.config(state="normal")
        self.log_text.insert("end", log_message + "\n")
        self.log_text.config(state="disabled")
        
        # Log to file as well
        with open(self.scan_log_file, "a") as log_file:
            log_file.write(log_message + "\n")
        
        self.log_text.yview("end")  # Scroll to the bottom of the log text box

    def send_email_log(self, subject, body):
        """Send the scan log as an email after scan completion."""
        try:
            msg = MIMEMultipart()
            msg['From'] = 'your_email@example.com'  # Set your email here
            msg['To'] = self.email_log
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Set up the server
            server = smtplib.SMTP('smtp.example.com', 587)  # SMTP server and port
            server.starttls()
            server.login('your_email@example.com', 'your_password')  # Login with your credentials
            text = msg.as_string()
            server.sendmail(msg['From'], msg['To'], text)
            server.quit()

            self.log(f"Log sent to email: {self.email_log}")
        except Exception as e:
            self.log(f"Error sending email: {str(e)}")

    def start_scan(self):
        """Starts the Scan process."""
        if self.running:
            msgbox.showinfo("Already Running", "Scan process is already in progress.")
            return

        # Check if target is provided
        target = self.target_entry.get().strip()
        if not target:
            msgbox.showwarning("Input Error", "Please enter a valid target domain or IP.")
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("Scan process started.")
        
        # Run the Scan process in a separate thread to prevent UI freezing
        threading.Thread(target=self.run_scan, args=(target,)).start()

    def stop_scan(self):
        """Stops the Scan process."""
        if not self.running:
            msgbox.showinfo("Not Running", "Scan is not currently running.")
            return

        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("Scan process stopped.")

    def run_scan(self, target):
        """Handles the execution of the Scan process using Nmap."""
        try:
            # Step 1: Perform selected Scan task
            scan_type = self.scan_type.get()
            if scan_type == "Port Scan":
                self.log("Starting Port Scan...")
                self.progress_bar.set(0.2)
                self.perform_port_scan(target)
            elif scan_type == "Service Scan":
                self.log("Starting Service Scan...")
                self.progress_bar.set(0.4)
                self.perform_service_scan(target)
            elif scan_type == "OS Scan":
                self.log("Starting OS Detection Scan...")
                self.progress_bar.set(0.6)
                self.perform_os_scan(target)
            
            self.progress_bar.set(1.0)
            self.log(f"{scan_type} completed successfully.")

            # Step 2: Send Email Log
            email_subject = f"{scan_type} Scan Log"
            with open(self.scan_log_file, "r") as log_file:
                log_content = log_file.read()
            self.send_email_log(email_subject, log_content)

            msgbox.showinfo("Scan Completed", f"{scan_type} Scan completed successfully.")
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            self.log(error_message)
            msgbox.showerror("Error", error_message)
        finally:
            # Reset UI state after completion or failure
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.progress_bar.set(0.0)  # Reset progress bar

    def perform_port_scan(self, target):
        """Performs a simple port scan using Nmap."""
        try:
            self.nm.scan(hosts=target, arguments='-p 22,80,443')
            self.log(f"Port Scan Results for {target}:\n{self.nm.all_hosts()}")
            for host in self.nm.all_hosts():
                self.log(f"Host: {host} ({self.nm[host].hostname()})")
                self.log(f"State: {self.nm[host].state()}")
                for proto in self.nm[host].all_protocols():
                    self.log(f"Protocol: {proto}")
                    lport = self.nm[host][proto].keys()
                    for port in lport:
                        self.log(f"Port: {port}\tState: {self.nm[host][proto][port]['state']}")
        except Exception as e:
            self.log(f"Error in Port Scan: {str(e)}")

    def perform_service_scan(self, target):
        """Performs a service version scan using Nmap."""
        try:
            self.nm.scan(hosts=target, arguments='-sV')
            self.log(f"Service Scan Results for {target}:\n{self.nm.all_hosts()}")
            for host in self.nm.all_hosts():
                self.log(f"Host: {host} ({self.nm[host].hostname()})")
                self.log(f"State: {self.nm[host].state()}")
                for proto in self.nm[host].all_protocols():
                    self.log(f"Protocol: {proto}")
                    lport = self.nm[host][proto].keys()
                    for port in lport:
                        self.log(f"Port: {port}\tState: {self.nm[host][proto][port]['state']}")
                        self.log(f"Service: {self.nm[host][proto][port]['name']} Version: {self.nm[host][proto][port]['version']}")
        except Exception as e:
            self.log(f"Error in Service Scan: {str(e)}")

    def perform_os_scan(self, target):
        """Performs an OS detection scan using Nmap."""
        try:
            self.nm.scan(hosts=target, arguments='-O')
            self.log(f"OS Scan Results for {target}:\n{self.nm.all_hosts()}")
            for host in self.nm.all_hosts():
                self.log(f"Host: {host} ({self.nm[host].hostname()})")
                self.log(f"OS: {self.nm[host]['osmatch'][0]['name']}")
        except Exception as e:
            self.log(f"Error in OS Scan: {str(e)}")

class ScannerTab:
    def __init__(self, parent):
        self.parent = parent
        self.running = False  # Flag to track if scanning is running
        self.scan_log_file = "scan_log.txt"  # Log file path
        self.email_log = "recipient@example.com"  # Email recipient for reports

        # Initialize the user interface (UI)
        self._setup_ui()

    def _setup_ui(self):
        """Sets up all UI elements for the Scanner Tab."""
        # Title Label
        ctk.CTkLabel(self.parent, text="Scanner - Network Scanning", font=("Segoe UI", 14)).pack(pady=(10, 4))

        # Instructions
        ctk.CTkLabel(self.parent, text="Click 'Start Scan' to perform scanning.", font=("Segoe UI", 12)).pack(pady=(10, 4))

        # Target Input
        ctk.CTkLabel(self.parent, text="Enter Target Domain or IP", font=("Segoe UI", 12)).pack(pady=(10, 4))
        self.target_entry = ctk.CTkEntry(self.parent, width=300)
        self.target_entry.pack(pady=(5, 20))

        # Start Button
        self.start_button = ctk.CTkButton(self.parent, text="Start Scan", command=self.start_scan, width=180)
        self.start_button.pack(pady=(10, 20))

        # Stop Button (Disabled initially)
        self.stop_button = ctk.CTkButton(self.parent, text="Stop Scan", command=self.stop_scan, width=180, state="disabled")
        self.stop_button.pack(pady=(10, 20))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.parent, width=500)
        self.progress_bar.pack(pady=(10, 20))

        # Log Display Area
        self.log_text = ctk.CTkTextbox(self.parent, width=500, height=200, state="disabled")
        self.log_text.pack(pady=(10, 20))

        # Scan Options
        self.scan_options_label = ctk.CTkLabel(self.parent, text="Select Scan Type", font=("Segoe UI", 12))
        self.scan_options_label.pack(pady=(10, 4))

        self.scan_type = ctk.CTkOptionMenu(self.parent, values=["Port Scan", "Vulnerability Scan"], width=200)
        self.scan_type.set("Port Scan")  # Default setting
        self.scan_type.pack(pady=(5, 20))

    def log(self, message):
        """Logs messages to both the log textbox and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        # Update the log display area
        self.log_text.config(state="normal")
        self.log_text.insert("end", log_message + "\n")
        self.log_text.config(state="disabled")
        
        # Log to file as well
        with open(self.scan_log_file, "a") as log_file:
            log_file.write(log_message + "\n")
        
        self.log_text.yview("end")  # Scroll to the bottom of the log text box

    def send_email_log(self, subject, body):
        """Send the scan log as an email after scan completion."""
        try:
            msg = MIMEMultipart()
            msg['From'] = 'your_email@example.com'  # Set your email here
            msg['To'] = self.email_log
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Set up the server
            server = smtplib.SMTP('smtp.example.com', 587)  # SMTP server and port
            server.starttls()
            server.login('your_email@example.com', 'your_password')  # Login with your credentials
            text = msg.as_string()
            server.sendmail(msg['From'], msg['To'], text)
            server.quit()

            self.log(f"Log sent to email: {self.email_log}")
        except Exception as e:
            self.log(f"Error sending email: {str(e)}")

    def start_scan(self):
        """Starts the Scan process."""
        if self.running:
            msgbox.showinfo("Already Running", "Scan process is already in progress.")
            return

        # Check if target is provided
        target = self.target_entry.get().strip()
        if not target:
            msgbox.showwarning("Input Error", "Please enter a valid target domain or IP.")
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("Scan process started.")
        
        # Run the Scan process in a separate thread to prevent UI freezing
        threading.Thread(target=self.run_scan, args=(target,)).start()

    def stop_scan(self):
        """Stops the Scan process."""
        if not self.running:
            msgbox.showinfo("Not Running", "Scan is not currently running.")
            return

        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("Scan process stopped.")

    def run_scan(self, target):
        """Handles the execution of the Scan process."""
        try:
            # Step 1: Perform selected Scan task
            scan_type = self.scan_type.get()
            if scan_type == "Port Scan":
                self.log("Starting Port Scan...")
                self.progress_bar.set(0.2)
                perform_port_scan(self, target)
            elif scan_type == "Vulnerability Scan":
                self.log("Starting Vulnerability Scan...")
                self.progress_bar.set(0.4)
                perform_vuln_scan(self, target)
            
            self.progress_bar.set(1.0)
            self.log(f"{scan_type} completed successfully.")

            # Step 2: Send Email Log
            email_subject = f"{scan_type} Scan Log"
            with open(self.scan_log_file, "r") as log_file:
                log_content = log_file.read()
            self.send_email_log(email_subject, log_content)

            msgbox.showinfo("Scan Completed", f"{scan_type} Scan completed successfully.")
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            self.log(error_message)
            msgbox.showerror("Error", error_message)
        finally:
            # Reset UI state after completion or failure
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.progress_bar.set(0.0)  # Reset progress bar
def load_scanner_tab(tab):
    def run_port_scan():
        target = scanner_target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a valid target IP or domain.")
            return

        scanner_output.delete("0.0", "end")
        scanner_output.insert("end", f"[*] Starting port scan on {target}...\n")
        status_label.configure(text="Status: Scanning...", fg="#28A745")

        def scan_worker():
            while not q.empty():
                port = q.get()
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)  # Timeout for each port scan
                        if s.connect_ex((target, port)) == 0:
                            scanner_output.insert("end", f"[+] Port {port} is open\n", "green")
                        else:
                            scanner_output.insert("end", f"[-] Port {port} is closed\n", "red")
                except Exception as e:
                    scanner_output.insert("end", f"[-] Error on port {port}: {e}\n", "yellow")
                q.task_done()

        top_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
                     1723, 3306, 3389, 5900, 8080, 8443, 8888, 8000, 8081, 8880, 10000, 9200,
                     5432, 389, 137, 138, 139, 2049, 1521, 465, 993, 995, 1025, 49152, 49153]

        q = Queue()
        for port in top_ports:
            q.put(port)

        for _ in range(100):
            threading.Thread(target=scan_worker, daemon=True).start()

        q.join()
        scanner_output.insert("end", "[*] Port scan finished.\n")
        status_label.configure(text="Status: Scan Complete", fg="#007BFF")

    def run_dir_scan():
        url = scanner_target_entry.get().strip().rstrip("/")
        if not url.startswith("http"):
            messagebox.showerror("Error", "Use full URL (http/https).")
            return

        scanner_output.insert("end", "\n[*] Starting directory scan...\n")
        status_label.configure(text="Status: Scanning directories...", fg="#28A745")

        wordlist = ["admin", "login", "dashboard", "config", "backup", "wp-admin",
                    "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"]

        def scan_path(path):
            full_url = f"{url}/{path}"
            try:
                r = requests.get(full_url, timeout=5)
                if r.status_code in [200, 301, 403]:
                    scanner_output.insert("end", f"[+] {full_url} [{r.status_code}]\n", "green")
                else:
                    scanner_output.insert("end", f"[-] {full_url} [{r.status_code}]\n", "red")
            except Exception:
                scanner_output.insert("end", f"[-] Error with path {full_url}\n", "yellow")

        threads = []
        for path in wordlist:
            t = threading.Thread(target=scan_path, args=(path,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        scanner_output.insert("end", "[*] Dir scan finished.\n")
        status_label.configure(text="Status: Directory Scan Complete", fg="#007BFF")

    # Header section with blue background color and padding
    header_frame = ctk.CTkFrame(tab, height=50, corner_radius=10, bg_color="#007BFF")  # Blue color
    header_frame.pack(fill="x", pady=(10, 5))

    # Title label inside the header with white text
    title_label = ctk.CTkLabel(header_frame, text="Scanner Tool", font=("Roboto", 20, "bold"), fg="#FFFFFF")
    title_label.pack(pady=10)

    # Status label with dynamic text that changes as scanning progresses
    status_label = ctk.CTkLabel(tab, text="Status: Idle", font=("Roboto", 14), fg="#FF4500")
    status_label.pack(pady=5)

    # Input field and buttons with padding for better layout
    ctk.CTkLabel(tab, text="Target IP or Domain", font=("Roboto", 14)).pack(pady=5)
    scanner_target_entry = ctk.CTkEntry(tab, width=500, font=("Roboto", 14))
    scanner_target_entry.pack(pady=5)

    # Action buttons with green background and hover effects
    ctk.CTkButton(tab, text="Start Port Scan", command=lambda: threading.Thread(target=run_port_scan).start(),
                  font=("Roboto", 14), fg_color="#28A745", hover_color="#218838").pack(pady=5)
    ctk.CTkButton(tab, text="Start Dir Scan", command=lambda: threading.Thread(target=run_dir_scan).start(),
                  font=("Roboto", 14), fg_color="#28A745", hover_color="#218838").pack(pady=5)

    # Output textbox with a nice border and scrollable feature
    scanner_output = ctk.CTkTextbox(tab, height=400, width=800, font=("Roboto", 12), wrap="word")
    scanner_output.pack(pady=10)

    # Optional scrollbar for better UX if the output exceeds the visible area
    scrollbar = ctk.CTkScrollbar(tab, command=scanner_output.yview)
    scrollbar.pack(side="right", fill="y")
    scanner_output.configure(yscrollcommand=scrollbar.set)

    # Adding custom tags to apply color coding to the output
    scanner_output.tag_configure("green", foreground="#28A745")
    scanner_output.tag_configure("red", foreground="#FF0000")
    scanner_output.tag_configure("yellow", foreground="#FFFF00")
