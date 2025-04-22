# top of main.py (imports section)
import os, time, socket, json, random
from queue import Queue
from datetime import datetime
from tkinter import messagebox, filedialog
import customtkinter as ctk
import requests, xmlrpc.client, tldextract
import threading
from urllib.parse import urljoin
import os
import sys
import threading
import customtkinter as ctk
from gui.dashboard import Dashboard
from gui.brute_tab import BruteTab
from gui.exploits_tab import ExploitsTab
from gui.auto_tab import AutoModeTab
from gui.reports_tab import ReportsTab
from gui.logs_tab import LogsTab
from gui.settings_tab import SettingsTab
from utils.logger import init_logger

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("X-Vector Pro | Cybersecurity Toolkit")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.setup_sidebar()
        self.setup_tabs()
        self.setup_status_bar()

        # Logger
        init_logger()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(self.sidebar, text="X-Vector Pro", font=("Arial Black", 20))
        self.logo.pack(pady=20)

        self.dark_mode_toggle = ctk.CTkSwitch(
            self.sidebar, text="Dark Mode", command=self.toggle_dark_mode
        )
        self.dark_mode_toggle.select()
        self.dark_mode_toggle.pack(pady=10)

    def setup_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="right", expand=True, fill="both")

        self.tabs = {
            "Dashboard": Dashboard(self.tabview),
            "AutoMode": AutoModeTab(self.tabview),
            "Brute": BruteTab(self.tabview),
            "Exploits": ExploitsTab(self.tabview),
            "Reports": ReportsTab(self.tabview),
            "Logs": LogsTab(self.tabview),
            "Settings": SettingsTab(self.tabview)
        }

        for name, frame in self.tabs.items():
            self.tabview.add(name)
            frame.pack(expand=True, fill="both")
            self.tabview.tab(name).configure(state="normal")

    def setup_status_bar(self):
        self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w", font=("Arial", 12))
        self.status_bar.pack(side="bottom", fill="x")

    def toggle_dark_mode(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "dark" else "dark")

    def on_exit(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
