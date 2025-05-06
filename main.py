import customtkinter as ctk
import logging
import os
from gui.tabs.recon_tab import ReconTab
from gui.tabs.brute_tab import BruteTab
from gui.tabs.exploit_tab import ExploitsTab
from gui.tabs.reports_tab import ReportsTab
from gui.tabs.ids_tab import IDSTab
from gui.tabs.auto_mode_tab import AutoModeTab
from gui.tabs.settings_tab import SettingsTab
from gui.tabs.cve_tab import CVETab
from gui.tabs.logs_tab import load_logs_tab
from urllib.parse import urljoin
import re
import xmlrpc.client
import importlib.util
from tkinter import filedialog, messagebox
import threading
import socket
from queue import Queue
import json
# Configure logging
LOG_FILE = "xvector_gui.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro - Cybersecurity Toolkit")
        self.geometry(self.get_window_geometry())
        self.configure_gui()

        # Create a tab view
        self.tab_view = ctk.CTkTabview(self, width=1280, height=960)
        self.tab_view.pack(expand=True, fill="both")

        # Add tabs
        self.add_tabs()

    def configure_gui(self):
        """Configure appearance and theme."""
        default_appearance = "dark"
        default_theme = "blue"

        # Optionally load appearance/theme from config.json
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    appearance = config.get("appearance", default_appearance)
                    theme = config.get("theme", default_theme)
            except Exception as e:
                logging.error(f"Error reading config.json: {e}")
                appearance, theme = default_appearance, default_theme
        else:
            appearance, theme = default_appearance, default_theme

        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(theme)
        logging.info(f"Appearance: {appearance}, Theme: {theme}")

    def get_window_geometry(self):
        """Adjust window size to 80% of screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)
        return f"{width}x{height}"

    def add_tabs(self):
        """Dynamically add all tabs."""
        tab_classes = {
            "Recon": ReconTab,
            "Brute Force": BruteTab,
            "Exploits": ExploitsTab,
            "Reports": ReportsTab,
            "IDS": IDSTab,
            "Auto Mode": AutoModeTab,
            "Settings": SettingsTab,
            "CVE Lookup": CVETab,
            "Logs": load_logs_tab  # loader function
        }

        for tab_name, TabClass in tab_classes.items():
            try:
                tab = self.tab_view.add(tab_name)
                if callable(TabClass):  # For loader function like logs_tab
                    TabClass(tab)
                else:
                    TabClass(tab)
                logging.info(f"{tab_name} tab loaded successfully.")
            except Exception as e:
                logging.error(f"Failed to load {tab_name} tab: {e}")

if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
