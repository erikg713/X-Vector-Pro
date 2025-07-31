import os
import customtkinter as ctk
import customtkinter as ctk
import customtkinter as ctk

def build_tab(parent):
    frame = ctk.CTkFrame(parent)

    title = ctk.CTkLabel(frame, text="Auto Mode", font=("Arial", 20, "bold"))
    title.pack(pady=(20, 10))

    desc = ctk.CTkLabel(frame, text="Automated Analysis Mode — Scan, Detect & Report Threats", wraplength=600, justify="center")
    desc.pack(pady=(0, 20))

    # Scan Target Input
    target_label = ctk.CTkLabel(frame, text="Target URL or IP:")
    target_label.pack(pady=(10, 0))
    target_entry = ctk.CTkEntry(frame, placeholder_text="http://example.com or 192.168.1.1", width=400)
    target_entry.pack(pady=5)

    # Wordlist Selector
    wordlist_label = ctk.CTkLabel(frame, text="Select Wordlist Type:")
    wordlist_label.pack(pady=(15, 0))
    wordlist_option = ctk.CTkOptionMenu(frame, values=["Scam Domains", "Phishing Keywords", "Flagged Users"])
    wordlist_option.pack(pady=5)

    # Auto Scan Button
    def handle_scan():
        target = target_entry.get()
        list_type = wordlist_option.get()
        result_label.configure(text=f"🕵️‍♂️ Scanning {target} using {list_type} wordlist...")

    scan_button = ctk.CTkButton(frame, text="Start Scan", command=handle_scan)
    scan_button.pack(pady=15)

    # Output Label
    result_label = ctk.CTkLabel(frame, text="", text_color="green", wraplength=500, justify="center")
    result_label.pack(pady=10)

    return frame

class AutoTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, text="Auto Mode: Full Recon, Scan, Brute Force")
        self.label.pack(pady=20)

        self.target_entry = ctk.CTkEntry(self, placeholder_text="Enter target URL")
        self.target_entry.pack(pady=10, padx=20, fill="x")

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_auto)
        self.start_button.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, height=200, width=600)
        self.output_box.pack(padx=20, pady=20, fill="both", expand=True)

    def start_auto(self):
        target = self.target_entry.get()
        self.output_box.insert("end", f"Starting full pipeline against {target}...\n")
        # Here you would kick off the full pipeline asynchronously, updating the output box

class AutoTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, text="Auto Mode: Full Recon, Scan, Brute Force")
        self.label.pack(pady=20)

        self.target_entry = ctk.CTkEntry(self, placeholder_text="Enter target URL")
        self.target_entry.pack(pady=10, padx=20, fill="x")

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_auto)
        self.start_button.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, height=200, width=600)
        self.output_box.pack(padx=20, pady=20, fill="both", expand=True)

    def start_auto(self):
        target = self.target_entry.get()
        self.output_box.insert("end", f"Starting full pipeline against {target}...\n")
        # Here you would kick off the full pipeline asynchronously, updating the output box

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HITS_FILE = os.path.join(BASE_DIR, "logs", "hits.txt")
SESSION_FILE = os.path.join(BASE_DIR, "logs", "session.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "xvector_log.txt")
WORDLIST_DIR = os.path.join(BASE_DIR, "wordlists")
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
        self._current_thread = None  # To track the current background thread

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

        # Progress Bar (shows progress of recon and exploitation)
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(pady=5, fill="x")
        self.progress.place_forget()  # Initially hidden

    def run_chain_threaded(self):
    target = self.target_var.get().strip()
    if not target or not self.is_valid_target(target):
        self.show_status("Enter a valid target.")
        return
    if self._current_thread and self._current_thread.is_alive():
        self.show_status("Another chain is still running.")
        return
    self._current_thread = threading.Thread(target=self.run_chain, args=(target,), daemon=True)
    self._current_thread.start()

def is_valid_target(self, target):
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    return re.match(ip_pattern, target) or re.match(domain_pattern, target)

        try:
            results = run_auto_chain(target, gui_callback=self.append_output)
            self.append_output(f"[INFO] Completed successfully.\n")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.set_button_state(True)
            self.show_progress(False)
            self.show_status("Idle")

    def append_output(self, text):
        """Optimized log display function to update output efficiently."""
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def show_status(self, text):
        """Optimized method for updating status with color coding."""
        self.status_var.set(text)

    def set_button_state(self, state: bool):
        """Optimized button state management to avoid redundancy."""
        self.run_button.configure(state="normal" if state else "disabled")

    def show_progress(self, show: bool):
        """Show or hide the progress bar based on the current operation status."""
        if show:
            self.progress.place(x=20, y=350)  # Position it appropriately
            self.progress.start()
        else:
            self.progress.place_forget()  # Hide the progress bar
            self.progress.stop()  # Stop the progress animation

    def clear_output(self):
        """Clear the output area."""
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def is_valid_target(self, target):
        """Improved target validation (IP or domain)."""
        # Combined validation for both IP and domain using regex
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$"
        
        if re.match(ip_pattern, target):
            return True
        if re.match(domain_pattern, target):
            return True
        return False

    def log_message(self, message, log_type="INFO"):
        """Centralized log function with enhanced levels."""
        if log_type == "INFO":
            self.append_output(f"[INFO] {message}\n")
        elif log_type == "WARNING":
            self.append_output(f"[WARNING] {message}\n")
        elif log_type == "ERROR":
            self.append_output(f"[ERROR] {message}\n")
import customtkinter as ctk

class AutoTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Auto Mode: Full Recon, Scan, Brute Force", font=("Segoe UI", 16))
        label.pack(pady=20)
        # Add your Auto mode widgets here


class ScanTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Scan Plugins: Enumerate Installed Plugins", font=("Segoe UI", 16))
        label.pack(pady=20)
        # Add your Scan mode widgets here


class XVectorProApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("X-Vector Pro")
        self.root.geometry("900x600")

        self.tab_view = ctk.CTkTabview(self.root)
        self.tab_view.pack(expand=True, fill="both")

        self.tab_view.add("Auto Mode")
        self.tab_view.add("Scan Plugins")

        self.auto_tab = AutoTab(self.tab_view)
        self.scan_tab = ScanTab(self.tab_view)

        self.tab_view.set("Auto Mode")

        # Pack the tabs inside their respective tab pages
        self.auto_tab.pack(expand=True, fill="both")
        self.scan_tab.pack(expand=True, fill="both")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = XVectorProApp()
    app.run()
