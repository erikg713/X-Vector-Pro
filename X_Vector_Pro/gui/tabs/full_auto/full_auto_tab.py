import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import os
from datetime import datetime
from gui.tabs.full_auto.auto_recon import run_auto_recon  # Importing the auto_recon function

class FullAutoTab:
    def __init__(self, master):
        self.master = master
        self.master.title("Full Auto Recon")
        self.master.geometry("600x400")

        # Frame for content
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        # Target IP/Domain Entry
        self.target_label = ttk.Label(self.frame, text="Enter Target IP/Domain:")
        self.target_label.pack(pady=10)

        self.target_entry = ttk.Entry(self.frame, width=40)
        self.target_entry.pack(pady=10)

        # Start Recon Button
        self.start_button = ttk.Button(self.frame, text="Start Full Auto Recon", command=self.start_full_auto_recon)
        self.start_button.pack(pady=20)

        # Output Log
        self.output_log = tk.Text(self.frame, height=10, width=70, wrap="word", state=tk.DISABLED)
        self.output_log.pack(pady=10)

    def start_full_auto_recon(self):
        # Get the target IP/domain from input
        target = self.target_entry.get().strip()

        if not target:
            messagebox.showerror("Input Error", "Please enter a valid target IP/domain.")
            return

        # Disable the entry and button while the scan is running
        self.target_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)

        # Create a new thread to run the recon without blocking the UI
        recon_thread = threading.Thread(target=self.run_recon, args=(target,))
        recon_thread.start()

    def run_recon(self, target):
        # Run the Auto Recon process
        self.log_output(f"Starting Full Auto Recon on {target}...\n")

        try:
            run_auto_recon(target)  # Call the auto recon function from the auto_recon module
            self.log_output(f"Full Auto Recon completed for {target}.\n")
            messagebox.showinfo("Recon Completed", f"Full Auto Recon completed for {target}.")
        except Exception as e:
            self.log_output(f"[!] Recon failed: {str(e)}\n")
            messagebox.showerror("Recon Failed", f"Error occurred: {str(e)}")
        finally:
            # Re-enable the input fields after the process completes
            self.target_entry.config(state=tk.NORMAL)
            self.start_button.config(state=tk.NORMAL)

    def log_output(self, text):
        # Log the output to the text box
        self.output_log.config(state=tk.NORMAL)
        self.output_log.insert(tk.END, text)
        self.output_log.yview(tk.END)  # Scroll to the bottom
        self.output_log.config(state=tk.DISABLED)

# Main Application window
if __name__ == "__main__":
    root = tk.Tk()
    app = FullAutoTab(root)
    root.mainloop()
