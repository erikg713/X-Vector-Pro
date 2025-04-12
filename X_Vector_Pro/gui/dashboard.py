from core.report import export_txt, export_html, export_pdf
import tkinter.filedialog as fd
import customtkinter as ctk
from pymongo import MongoClient
from core.recon import run_auto_recon
from utils.logger import log
import threading

class XVectorDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro Dashboard")
        self.geometry("1024x700")
        self.build_gui()

    def build_gui(self):
        self.recon_view = ReconViewer(self)
        self.recon_view.pack(fill="both", expand=True)

        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", pady=8)

        self.entry = ctk.CTkEntry(bottom, placeholder_text="Enter target IP/domain...")
        self.entry.pack(side="left", padx=5, expand=True, fill="x")

        ctk.CTkButton(bottom, text="Run Auto Recon", command=self.run_recon_threaded).pack(side="left", padx=5)

    def run_recon_threaded(self):
        target = self.entry.get().strip()
        if not target:
            return
        threading.Thread(target=self.run_recon, args=(target,), daemon=True).start()

    def run_recon(self, target):
        log(f"[GUI] Running recon on {target}")
        run_auto_recon(target)
        self.recon_view.load_all()

class ReconViewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["xvector"]
        self.col = self.db["auto_recon"]
        self.build_ui()

    def build_ui(self):
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", pady=10, padx=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by IP or timestamp...")
        self.search_entry.pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkButton(search_frame, text="Search", command=self.search).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Load All", command=self.load_all).pack(side="left", padx=5)

        self.result_box = ctk.CTkTextbox(self, wrap="word")
        self.result_box.pack(expand=True, fill="both", padx=10, pady=10)
export_frame = ctk.CTkFrame(self)
export_frame.pack(fill="x", padx=10)

ctk.CTkButton(export_frame, text="Export TXT", command=self.export_txt).pack(side="left", padx=5)
ctk.CTkButton(export_frame, text="Export HTML", command=self.export_html).pack(side="left", padx=5)
ctk.CTkButton(export_frame, text="Export PDF", command=self.export_pdf).pack(side="left", padx=5)

self.filter_open = ctk.CTkCheckBox(export_frame, text="Open Only", command=self.apply_filter)
self.filter_open.pack(side="right", padx=5)
    def display(self, data):
        self.result_box.delete("1.0", "end")
        if not data:
            self.result_box.insert("end", "No results found.\n")
            return

        for scan in data:
            self.result_box.insert("end", f"Target: {scan['target']}\n")
            self.result_box.insert("end", f"Timestamp: {scan['timestamp']}\n")
            self.result_box.insert("end", "Ports:\n")
            for host in scan.get("summary", []):
                self.result_box.insert("end", f"  Host: {host['ip']}\n")
                for port in host["ports"]:
                    self.result_box.insert("end", f"    - {port}\n")
            self.result_box.insert("end", "-"*60 + "\n")

    def search(self):
        term = self.search_entry.get()
        q = {"$or": [
            {"target": {"$regex": term, "$options": "i"}},
            {"timestamp": {"$regex": term, "$options": "i"}}
        ]}
        data = list(self.col.find(q).sort("timestamp", -1))
        self.display(data)

    def load_all(self):
        data = list(self.col.find().sort("timestamp", -1))
        self.display(data)
