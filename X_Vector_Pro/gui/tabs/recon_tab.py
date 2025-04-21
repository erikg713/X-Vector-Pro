# gui/tabs/recon_tab.py

import customtkinter as ctk
import threading
from core.recon.recon_engine import run_recon  # Hook to recon logic
from utils.logger import log

class ReconTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Reconnaissance", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Target IP/domain...")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.run_button = ctk.CTkButton(input_frame, text="Run Recon", command=self.run_recon_threaded)
        self.run_button.pack(side="left")

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Recon results will appear here...\n")
        self.output_box.configure(state="disabled")

    def run_recon_threaded(self):
        target = self.target_var.get().strip()
        if not target:
            self.show_status("Enter a valid target.")
            return
        threading.Thread(target=self.run_recon, args=(target,), daemon=True).start()

    def run_recon(self, target):
        self.show_status(f"Running reconnaissance on {target}...")
        self.set_button_state(False)

        self.append_output(f"[INFO] Starting recon on {target}\n")
        try:
            results = run_recon(target, gui_callback=self.append_output)
            self.append_output(f"[INFO] Recon complete.\n")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")

    def append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)

    def set_button_state(self, state: bool):
        self.run_button.configure(state="normal" if state else "disabled")

import customtkinter as ctk
from pymongo import MongoClient

class ReconViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro - Recon Viewer")
        self.geometry("800x600")

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["xvector"]
        self.collection = self.db["auto_recon"]

        self.build_gui()

    def build_gui(self):
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(padx=10, pady=10, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Enter IP or timestamp...")
        self.search_entry.pack(side="left", expand=True, fill="x", padx=5)

        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.search_scan)
        self.search_button.pack(side="left", padx=5)

        self.refresh_button = ctk.CTkButton(self.search_frame, text="Load All", command=self.load_all_scans)
        self.refresh_button.pack(side="left", padx=5)

        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_box = ctk.CTkTextbox(self.results_frame, wrap="word")
        self.results_box.pack(fill="both", expand=True)

    def display_results(self, scans):
        self.results_box.delete("1.0", "end")
        if not scans:
            self.results_box.insert("end", "No scans found.")
            return

        for scan in scans:
            self.results_box.insert("end", f"Target: {scan['target']}\n")
            self.results_box.insert("end", f"Timestamp: {scan['timestamp']}\n")
            self.results_box.insert("end", "Ports:\n")
            for host in scan.get("summary", []):
                self.results_box.insert("end", f"  Host: {host['ip']}\n")
                for port in host["ports"]:
                    self.results_box.insert("end", f"    - {port}\n")
            self.results_box.insert("end", "-" * 60 + "\n")

    def search_scan(self):
        keyword = self.search_entry.get().strip()
        query = {
            "$or": [
                {"target": {"$regex": keyword, "$options": "i"}},
                {"timestamp": {"$regex": keyword, "$options": "i"}}
            ]
        }
        results = list(self.collection.find(query).sort("timestamp", -1))
        self.display_results(results)

    def load_all_scans(self):
        results = list(self.collection.find().sort("timestamp", -1))
        self.display_results(results)

if __name__ == "__main__":
    app = ReconViewerApp()
    app.mainloop()
