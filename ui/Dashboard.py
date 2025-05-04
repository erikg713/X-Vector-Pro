# X_Vector_Pro/ui/dashboard.py

import tkinter as tk
from tkinter import ttk
from ui.tabs.auto_tab import AutoTab
from ui.tabs.brute_tab import BruteTab
from ui.tabs.exploits_tab import ExploitsTab
from ui.tabs.reports_tab import ReportsTab
from ui.tabs.logs_tab import LogsTab
from ui.theme import apply_dark_theme
from ui.notifications import ToastManager

class Dashboard:
    def __init__(self):
        self.root = None
        self.tab_control = None
        self.toast = ToastManager()
        self.tabs = {}

    def inject(self, root):
        self.root = root
        self.root.title("X-Vector Pro")
        self.root.configure(bg="#1e1e1e")
        apply_dark_theme(self.root)

        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        self._load_tabs()
        self.toast.attach(self.root)

    def _load_tabs(self):
        self.tabs["Auto"] = AutoTab(self.tab_control, self.toast)
        self.tabs["Brute"] = BruteTab(self.tab_control, self.toast)
        self.tabs["Exploits"] = ExploitsTab(self.tab_control, self.toast)
        self.tabs["Reports"] = ReportsTab(self.tab_control, self.toast)
        self.tabs["Logs"] = LogsTab(self.tab_control, self.toast)

        for name, tab in self.tabs.items():
            self.tab_control.add(tab.frame, text=name)
