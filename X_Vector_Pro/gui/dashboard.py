# gui/dashboard.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from gui.tabs.brute_tab import BruteTab
from gui.tabs.recon_tab import ReconTab
from gui.tabs.scanner_tab import ScannerTab
from gui.tabs.ids_tab import IDSTab
from gui.tabs.exploit_tab import ExploitTab
from gui.tabs.auto_mode_tab import AutoModeTab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

TAB_CLASSES = {
    "Brute Force": BruteTab,
    "Recon": ReconTab,
    "Scanner": ScannerTab,
    "IDS": IDSTab,
    "Exploits": ExploitTab,
    "Auto Mode": AutoModeTab
}

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1200x800")
        self.minsize(1024, 700)
        self.active_tab = None
        self.frames = {}

        self.build_sidebar()
        self.build_content()

    def build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=180, fg_color="#1a1a1a")
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="X-Vector Pro", font=("Arial", 20, "bold")).pack(pady=20)

        for tab_name in TAB_CLASSES:
            ctk.CTkButton(sidebar, text=tab_name, command=lambda name=tab_name: self.switch_tab(name)).pack(padx=10, pady=5, fill="x")

    def build_content(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

    def switch_tab(self, name):
        if self.active_tab:
            self.active_tab.destroy()

        tab_class = TAB_CLASSES[name]
        self.active_tab = tab_class(self.content_frame)
        self.active_tab.pack(fill="both", expand=True)
