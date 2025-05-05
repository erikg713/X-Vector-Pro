import customtkinter as ctk
import threading
from core.auto_chain import run_auto_chain  # Ensure this function is implemented
from utils.logger import log  # Optional logging, use inside try/except as needed

class FullAutoTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()
        self._current_thread = None  # To track the current background thread

    def build_ui(self):
        # Title Label
        ctk.CTkLabel(self, text="Full Automated Recon + Exploit", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        # Input Frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        # Target Entry
        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Enter target IP or domain...")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Start Button
        self.run_button = ctk.CTkButton(input_frame, text="Run Full Auto", command=self.run_chain_threaded)
        self.run_button.pack(side="left")

        # Status Label
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        # Output Box (for logs)
        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Logs will appear here...\n")
        self.output_box.configure(state="disabled")

        # Clear Output Button
        self.clear_button = ctk.CTkButton(self, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(pady=(5, 10))

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(pady=5, fill="x")
        self.progress.place_forget()  # Initially hidden

    def run_chain_threaded(self):
        target = self.target_var.get().strip()
        if not target or not self.is_valid_target(target):
            self.show_status("Enter a valid target.")
            return
        if self._current_thread and self._current_thread.is_alive():
            self.show_status("Another operation is in progress.")
            return
        threading.Thread(target=self.run_chain, args=(target,), daemon=True).start()

    def run_chain(self, target):
        self.show_status(f"Running full automation on {target}...")
        self.set_button_state(False)
        self.show_progress(True)
        self.append_output(f"[INFO] Starting full chain on {target}\n")
        
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
        """Efficient method to append output to the log box."""
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def show_status(self, text):
        """Update the status label."""
        self.status_var.set(text)

    def set_button_state(self, state: bool):
        """Toggle button state between enabled/disabled."""
        self.run_button.configure(state="normal" if state else "disabled")

    def show_progress(self, show: bool):
        """Show or hide the progress bar."""
        if show:
            self.progress.place(x=20, y=350)  # Position it appropriately
            self.progress.start()
        else:
            self.progress.place_forget()  # Hide the progress bar
            self.progress.stop()

    def clear_output(self):
        """Clear the output textbox."""
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def is_valid_target(self, target):
        """Validate the target (IP or domain)."""
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$"
        
        if re.match(ip_pattern, target):
            return True
        if re.match(domain_pattern, target):
            return True
        return False
