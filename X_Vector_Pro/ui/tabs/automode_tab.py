import customtkinter as ctk
import threading
import time
from datetime import datetime
from utils.logger import log_to_central
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.email_config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS

class AutoModeTab:
    def __init__(self, parent):
        self.parent = parent
        self.execution_history = {}
        self.current_task = None

        # Initialize UI components
        self._setup_ui()

    def _setup_ui(self):
        # Title Label
        ctk.CTkLabel(self.parent, text="Auto Mode - Recon -> Scan -> Exploit", font=("Segoe UI", 14)).pack(pady=(10, 4))

        # Target Input
        ctk.CTkLabel(self.parent, text="Target IP or Domain", font=("Segoe UI", 12)).pack(pady=(10, 4))
        self.target_entry = ctk.CTkEntry(self.parent, width=500)
        self.target_entry.pack(pady=(0, 10))

        # Output console for logs
        self.output_console = ctk.CTkTextbox(self.parent, width=900, height=420, font=("Consolas", 12))
        self.output_console.pack(pady=10)

        # Auto Mode Button
        self.start_button = ctk.CTkButton(
            self.parent,
            text="Start Auto Mode",
            command=self._start_auto_mode,
            fg_color="#1f6feb",
            hover_color="#1953c5",
            width=180
        )
        self.start_button.pack(pady=(5, 10))

        # Progress bar for task completion
        self.progress_bar = ctk.CTkProgressBar(self.parent, width=800, height=30)
        self.progress_bar.pack(pady=(10, 20))

    def _log(self, message):
        """Log messages to the output console and log file."""
        self.output_console.insert("end", f"{message}\n")
        self.output_console.see("end")

        # Optionally save log message to file
        with open("automode_report.txt", "a") as f:
            f.write(f"{message}\n")

    def _start_auto_mode(self):
        """Start the auto mode process: Recon -> Scan -> Exploit -> Report"""
        target = self.target_entry.get().strip()
        if not target:
            ctk.messagebox.showwarning("Target Missing", "Please enter a valid target IP or domain.")
            return

        self._log("[*] Starting Auto Mode...\n")
        self._log(f"[*] Target: {target}\n")

        # Disable start button while process is running
        self.start_button.configure(state="disabled")

        # Start the task in a separate thread to allow UI updates
        self.current_task = threading.Thread(target=self._auto_mode_task, args=(target,))
        self.current_task.start()

    def _auto_mode_task(self, target):
        """The main task of Auto Mode - Running Recon -> Scan -> Exploit."""
        try:
            # Step 1: Recon
            self._log("[*] Starting Recon...\n")
            recon_result = self._perform_recon(target)
            if not recon_result:
                self._log("[-] Recon failed.")
                return

            self._log(f"[*] Recon completed. Found information: {recon_result}\n")

            # Step 2: Scan
            self._log("[*] Starting Scan...\n")
            scan_result = self._perform_scan(target, recon_result)
            if not scan_result:
                self._log("[-] Scan failed.")
                return

            self._log(f"[*] Scan completed. Detected vulnerabilities: {scan_result}\n")

            # Step 3: Exploit
            self._log("[*] Starting Exploit...\n")
            exploit_result = self._perform_exploit(target, scan_result)
            if not exploit_result:
                self._log("[-] Exploit failed.")
                return

            self._log(f"[*] Exploit completed. Exploited vulnerabilities: {exploit_result}\n")

            # Step 4: Report Generation
            self._log("[*] Generating Report...\n")
            self._generate_report(target, recon_result, scan_result, exploit_result)

            # Send email after completion
            self._send_report_email(target, recon_result, scan_result, exploit_result)

        except Exception as e:
            self._log(f"[!] AutoMode error: {e}")
        finally:
            self.start_button.configure(state="normal")  # Enable the button after the task is complete

    def _perform_recon(self, target):
        """Perform a recon on the target (basic info gathering, port scan, etc.)."""
        try:
            # Simulating the recon phase
            self._log("[*] Recon: Gathering target information...")
            time.sleep(3)  # Simulate network scan
            self.progress_bar.set(0.25)  # Update progress
            return {"open_ports": [80, 443], "services": ["HTTP", "HTTPS"], "os": "Linux"}
        except Exception as e:
            self._log(f"[!] Recon error: {e}")
            return None

    def _perform_scan(self, target, recon_result):
        """Perform a scan based on recon information (vulnerability detection)."""
        try:
            # Simulating the scan phase
            self._log("[*] Scan: Checking for vulnerabilities...")
            time.sleep(3)  # Simulate vulnerability scan
            self.progress_bar.set(0.5)  # Update progress
            return {"vulnerabilities": ["CVE-2020-1234", "CVE-2021-2345"]}
        except Exception as e:
            self._log(f"[!] Scan error: {e}")
            return None

    def _perform_exploit(self, target, scan_result):
        """Perform an exploit based on the scanned vulnerabilities."""
        try:
            # Simulating the exploit phase
            self._log("[*] Exploit: Attempting to exploit vulnerabilities...")
            time.sleep(3)  # Simulate exploit attempt
            self.progress_bar.set(0.75)  # Update progress
            return {"exploited_vulnerabilities": scan_result["vulnerabilities"]}
        except Exception as e:
            self._log(f"[!] Exploit error: {e}")
            return None

    def _generate_report(self, target, recon_result, scan_result, exploit_result):
        """Generate and log the final report after completing the full Auto Mode process."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_content = f"""
        [*] Auto Mode Report - {timestamp}
        Target: {target}
        
        [*] Recon Results:
        Open Ports: {recon_result['open_ports']}
        Services: {recon_result['services']}
        Operating System: {recon_result['os']}
        
        [*] Scan Results:
        Vulnerabilities: {scan_result['vulnerabilities']}
        
        [*] Exploit Results:
        Exploited Vulnerabilities: {exploit_result['exploited_vulnerabilities']}
        
        [*] Auto Mode Process Completed.
        """
        self._log(report_content)

        # Optionally, send the report via email or store it for future reference
        self._save_report(report_content)

    def _save_report(self, report_content):
        """Save the report to a file."""
        with open(f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "w") as f:
            f.write(report_content)

    def _send_report_email(self, target, recon_result, scan_result, exploit_result):
        """Send the generated report via email."""
        try:
            # Create the email content
            report_content = f"""
            Auto Mode Report for Target: {target}
            Recon: {recon_result}
            Scan: {scan_result}
            Exploit: {exploit_result}
            """
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = EMAIL_USER
            msg['Subject'] = f"Auto Mode Report - {target}"

            body = MIMEText(report_content, 'plain')
            msg.attach(body)

            # Send the email
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())

            self._log("[*] Report sent via email.")
        except Exception as e:
            self._log(f"[!] Failed to send report email: {e}")
