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
