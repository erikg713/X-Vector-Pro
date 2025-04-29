import customtkinter as ctk
from ui.tabs.recon_tab import load_recon_tab
from ui.tabs.scanner_tab import load_scanner_tab
from ui.tabs.brute_force_tab import load_brute_force_tab
from ui.tabs.exploits_tab import load_exploits_tab
from ui.tabs.reports_tab import load_reports_tab
from ui.tabs.settings_tab import load_settings_tab

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, settings):
        super().__init__(master)
        
        # Set up the dashboard layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a tab container
        self.tab_container = ctk.CTkNotebook(self)
        self.tab_container.grid(row=0, column=0, sticky="nsew")

        # Load all tabs
        load_recon_tab(self.tab_container)
        load_scanner_tab(self.tab_container)
        load_brute_force_tab(self.tab_container)
        load_exploits_tab(self.tab_container)
        load_reports_tab(self.tab_container)
        load_settings_tab(self.tab_container, settings)
