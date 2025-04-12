import customtkinter as ctk
from pymongo import MongoClient

class ScanHistoryTimeline(ctk.CTkFrame):
    def __init__(self, master, load_callback):
        super().__init__(master)
        self.load_callback = load_callback
        self.client = MongoClient("mongodb://localhost:27017/")
        self.col = self.client["xvector"]["auto_recon"]

        self.build_ui()
        self.load_timeline()

    def build_ui(self):
        self.listbox = ctk.CTkTextbox(self, width=300)
        self.listbox.pack(side="left", fill="y", padx=5, pady=5)

        self.listbox.bind("<Double-1>", self.load_selected)

        self.scrollbar = ctk.CTkScrollbar(self)
        self.scrollbar.pack(side="left", fill="y")

    def load_timeline(self):
        self.listbox.delete("1.0", "end")
        self.entries = list(self.col.find().sort("timestamp", -1))
        for idx, scan in enumerate(self.entries):
            line = f"{idx+1}. {scan['timestamp']} — {scan['target']}\n"
            self.listbox.insert("end", line)

    def load_selected(self, _):
        index = int(self.listbox.index("insert").split(".")[0]) - 1
        if 0 <= index < len(self.entries):
            self.load_callback([self.entries[index]])
