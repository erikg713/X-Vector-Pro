import tkinter as tk
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox
from engine.network.tor_detector import run_detection

class TorTab(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = CTkLabel(self, text="Tor Detector")
        self.label.pack(pady=10)

        self.entry = CTkEntry(self, width=400, placeholder_text="Enter IP or domain...")
        self.entry.pack(pady=5)

        self.button = CTkButton(self, text="Run Detection", command=self.detect)
        self.button.pack(pady=5)

        self.output = CTkTextbox(self, height=200)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def detect(self):
        target = self.entry.get()
        result = run_detection(target)
        self.output.delete("0.0", "end")
        self.output.insert("0.0", f"{result['status'].upper()}:\n{result['message']}\n\n{result['details']}")
