import customtkinter as ctk
from core.recon.history import get_recon_history

class ReconHistoryTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.history_box = ctk.CTkTextbox(self, width=800, height=500)
        self.history_box.pack(padx=20, pady=20)
        self.refresh_button = ctk.CTkButton(self, text="Refresh History", command=self.load_history)
        self.refresh_button.pack(pady=10)
        self.load_history()

    def load_history(self):
        self.history_box.delete("1.0", "end")
        history = get_recon_history()
        if not history:
            self.history_box.insert("end", "No recon history available.")
            return

        for entry in history:
            timestamp = entry.get("timestamp", "unknown")
            target = entry.get("target", "unknown")
            summary = entry.get("summary", [])
            self.history_box.insert("end", f"\n[{timestamp}] Target: {target}\n")
            for port_info in summary:
                ip = port_info.get("ip", "unknown")
                ports = "\n".join(f"  - {p}" for p in port_info.get("ports", []))
                self.history_box.insert("end", f"  Host: {ip}\n{ports}\n")
            self.history_box.insert("end", "-" * 60 + "\n")
