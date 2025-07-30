import customtkinter as ctk
import os
from ui.tabs_brute import load_brute_tab
from ui.tabs_recon import load_recon_tab
from ui.tabs_scanner import load_scanner_tab
from ui.tabs_exploits import load_exploit_tab
from ui.tabs_logs import load_logs_tab
from ui.tabs_settings import load_settings_tab
from ui.tabs_fullauto import load_fullauto_tab
from ui.tabs_findings import load_findings_tab
from PyQt5.QtWidgets import QTabWidget
# core/tabs.py
from PyQt5.QtWidgets import QTabWidget
# … existing imports …
from core.gui_bruteforce import BruteForceTab

class MainTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # … your other tabs …
        self.addTab(BruteForceTab(), "Brute-Force")

from core.gui_bruteforce import BruteForceTab

class MainTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # … your other tabs …
        self.addTab(BruteForceTab(), "Brute-Force")

def init_tabs(tabs, app, settings):
    """
    Initializes the tabs and loads the content for each tab.
    
    Args:
        tabs (ctk.CTkTabview): The tabview object where tabs will be added.
        app: The main application object.
        settings: The settings object to configure the settings tab.
    """
    tab_names = [
        ("Recon", load_recon_tab),
        ("Scanner", load_scanner_tab),
        ("Brute Force", load_brute_tab),
        ("Exploits", load_exploit_tab),
        ("Logs", load_logs_tab),
        ("Settings", load_settings_tab, settings),
        ("Full Auto", load_fullauto_tab),
        ("Findings", load_findings_tab)
    ]
    
    # Create and load content into each tab
    for tab_name, load_func, *args in tab_names:
        try:
            tab = tabs.add(tab_name)
            load_func(tab, *args)  # Dynamically load content into the tab
        except Exception as e:
            print(f"Error loading tab '{tab_name}': {e}")
            continue  # Optionally handle tab load errors gracefully

# Example usage
# Assuming `tabs` is an instance of CTkTabview and `settings` is a settings object
# init_tabs(tabs, app, settings)
