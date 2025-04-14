import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os

from utils.logger import log_to_central
from utils.settings import load_settings
from utils.splash import show_splash_screen
from core.recon.recon_engine import ReconEngine
from gui.dashboard import ReconViewer
from ui.tabs import init_tabs

class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro | Silent. Adaptive. Lethal.")
        self.geometry("1024x700")

        # Appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Show splash
        show_splash_screen()

        # Recon Viewer
        self.recon_viewer = ReconViewer(self)
        self.recon_viewer.pack(fill="both", expand=True)

        # Tab view
        self.tabs = ctk.CTkTabview(self, width=980, height=620)
        self.tabs.pack(padx=10, pady=10)

        # Load settings and initialize UI tabs
        settings = load_settings()
        init_tabs(self.tabs, self, settings)

def launch_gui():
    app = XVectorGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()
