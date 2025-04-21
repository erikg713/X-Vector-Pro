import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from gui.tabs.full_auto.auto_recon import run_auto_recon

class FullAutoTab:
    def __init__(self, master):
        self.master = master
        self.master.title("Full Auto Recon")
        self.master.geometry("700x520")

        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Target IP/Domain Input
        self.target_label = ttk.Label(self.frame, text="Target IP or Domain:")
        self.target_label.pack(pady=(0, 5))
        self.target_entry = ttk.Entry(self.frame, width=50)
        self.target_entry.pack()

        # Optional Folder Name Input
        self.dir_label = ttk.Label(self.frame, text="Optional Custom Output Folder:")
        self.dir_label.pack(pady=(15, 5))
        self.dir_entry = ttk.Entry(self.frame, width=50)
        self.dir_entry.pack()

        # Start Button
        self.start_button = ttk.Button(self.frame, text="Run Full Auto Recon", command=self.start_full_auto_recon)
        self.start_button.pack(pady=20)

        # Output Log Textbox
        self.output_log = tk.Text(self.frame, height=15, width=85, wrap="word", state=tk.DISABLED)
        self.output_log.pack(pady=10)

    def start_full_auto_recon(self):
        target = self.target_entry.get().strip()
        custom_dir = self.dir_entry.get().strip()

        if not target:
            messagebox.showerror("Input Error", "Please enter a valid target.")
            return

        # Disable inputs while running
        self.target_entry.config(state=tk.DISABLED)
        self.dir_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)

        # Start threaded recon
        threading.Thread(target=self.run_recon, args=(target, custom_dir)).start()

    def run_recon(self, target, custom_dir):
        self.log_output(f"\n[+] Starting Full Auto Recon on {target}...\n")

        output_dir = None
        if custom_dir:
            output_dir = os.path.join("reports", "auto_recon", custom_dir.replace(" ", "_"))

        try:
            result = run_auto_recon(target, output_dir)

            if result.get("status") == "success":
                self.log_output(f"[✓] Recon Complete for {target}")
                self.log_output(f"Output Directory: {result['output_dir']}")
                self.log_output(f"Scan Files: {result['filename']}.*\n")

                self.log_output("[Summary Results:]")
                for host in result["summary"]:
                    self.log_output(f"Host: {host['ip']}")
                    for port in host["ports"]:
                        self.log_output(f"  - {port}")

                messagebox.showinfo("Recon Complete", f"Recon completed. Output saved to:\n{result['output_dir']}")
            else:
                self.log_output(f"[!] Recon failed: {result.get('error', 'Unknown error')}")
                messagebox.showerror("Recon Error", result.get("error", "Unknown error"))

        except Exception as e:
            self.log_output(f"[!] Exception during recon: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Re-enable inputs
        self.target_entry.config(state=tk.NORMAL)
        self.dir_entry.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)

    def log_output(self, text):
        self.output_log.config(state=tk.NORMAL)
        self.output_log.insert(tk.END, text + "\n")
        self.output_log.yview(tk.END)
        self.output_log.config(state=tk.DISABLED)

# For standalone testing
if __name__ == "__main__":
    root = tk.Tk()
    app = FullAutoTab(root)
    root.mainloop()
