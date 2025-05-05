import customtkinter as ctk
import time
from datetime import datetime
from utils.logger import log_to_central
from utils.automode_utils import run_recon, run_scan, run_exploit, generate_report
import tkinter.messagebox as msgbox
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AutoModeTab:
    def __init__(self, parent):
        self.parent = parent
        self.running = False  # Flag to track if AutoMode is running
        self.log_file = "automode_log.txt"  # Path for log file
        self.email_log = "recipient@example.com"  # Set your desired email recipient here
        
        # Initialize the user interface (UI)
        self._setup_ui()

    def _setup_ui(self):
        """Sets up all UI elements for the AutoMode Tab."""
        # Title Label
        ctk.CTkLabel(self.parent, text="AutoMode - Automated Recon, Scan, Exploit", font=("Segoe UI", 14)).pack(pady=(10, 4))

        # Instructions
        ctk.CTkLabel(self.parent, text="Click 'Start AutoMode' to run automated tasks.", font=("Segoe UI", 12)).pack(pady=(10, 4))

        # Start Button
        self.start_button = ctk.CTkButton(self.parent, text="Start AutoMode", command=self.start_automode, width=180)
        self.start_button.pack(pady=(10, 20))

        # Stop Button (Disabled initially)
        self.stop_button = ctk.CTkButton(self.parent, text="Stop AutoMode", command=self.stop_automode, width=180, state="disabled")
        self.stop_button.pack(pady=(10, 20))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.parent, width=500)
        self.progress_bar.pack(pady=(10, 20))

        # Log Display Area
        self.log_text = ctk.CTkTextbox(self.parent, width=500, height=200, state="disabled")
        self.log_text.pack(pady=(10, 20))

        # AutoMode Settings Section (e.g., scan intensity)
        self.scan_intensity_label = ctk.CTkLabel(self.parent, text="Scan Intensity", font=("Segoe UI", 12))
        self.scan_intensity_label.pack(pady=(10, 4))

        self.scan_intensity = ctk.CTkOptionMenu(self.parent, values=["Low", "Medium", "High"], width=200)
        self.scan_intensity.set("Medium")  # Default setting
        self.scan_intensity.pack(pady=(5, 20))

    def log(self, message):
        """Logs messages to both the log textbox and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        # Update the log display area
        self.log_text.config(state="normal")
        self.log_text.insert("end", log_message + "\n")
        self.log_text.config(state="disabled")
        
        # Log to file as well
        with open(self.log_file, "a") as log_file:
            log_file.write(log_message + "\n")
        
        self.log_text.yview("end")  # Scroll to the bottom of the log text box

    def send_email_log(self, subject, body):
        """Send the log as an email after AutoMode completion."""
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

    def start_automode(self):
        """Starts the AutoMode process: Recon -> Scan -> Exploit -> Report."""
        if self.running:
            msgbox.showinfo("Already Running", "AutoMode is already in progress.")
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("AutoMode started.")
        
        # Run the AutoMode process in a separate thread to prevent UI freezing
        threading.Thread(target=self.run_automode).start()

    def stop_automode(self):
        """Stops the AutoMode process."""
        if not self.running:
            msgbox.showinfo("Not Running", "AutoMode is not currently running.")
            return

        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("AutoMode stopped.")

    def run_automode(self):
        """Handles the execution of AutoMode steps: Recon -> Scan -> Exploit -> Report."""
        try:
            # Step 1: Run Recon
            self.log("Starting Recon phase...")
            self.progress_bar.set(0.0)
            run_recon(self)
            self.progress_bar.set(0.25)
            self.log("Recon phase completed.")

            # Step 2: Run Scan
            self.log("Starting Scan phase...")
            self.progress_bar.set(0.5)
            run_scan(self, self.scan_intensity.get())
            self.progress_bar.set(0.75)
            self.log("Scan phase completed.")

            # Step 3: Run Exploit
            self.log("Starting Exploit phase...")
            run_exploit(self)
            self.progress_bar.set(1.0)
            self.log("Exploit phase completed.")

            # Step 4: Generate Report
            self.log("Generating report...")
            generate_report(self)
            self.log("Report generated successfully.")
            
            # Send email with logs
            email_subject = "AutoMode Completion Log"
            with open(self.log_file, "r") as log_file:
                log_content = log_file.read()
            self.send_email_log(email_subject, log_content)

            msgbox.showinfo("AutoMode Completed", "AutoMode process completed successfully.")
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
