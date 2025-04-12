import customtkinter as ctk
from pymongo import MongoClient

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
            self.result_box.insert("end", "-"*50 + "\n")

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

# Launchable standalone for dev/test
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("X-Vector Pro - Recon Viewer")
    app.geometry("1024x700")
    ReconViewer(app).pack(fill="both", expand=True)
    app.mainloop()
