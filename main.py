import customtkinter as ctk
from gui.tabs.recon_tab import ReconTab
from gui.tabs.brute_tab import BruteTab
from gui.tabs.exploit_tab import ExploitsTab
from gui.tabs.reports_tab import ReportsTab
from gui.tabs.ids_tab import IDSTab
from gui.tabs.auto_mode_tab import AutoModeTab
from gui.tabs.settings_tab import SettingsTab

# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro - Cybersecurity Toolkit")
        self.geometry("1024x768")

        # Create a tab view
        self.tab_view = ctk.CTkTabview(self, width=1024, height=768)
        self.tab_view.pack(expand=True, fill="both")

        # Add tabs
        self.add_tabs()

    def add_tabs(self):
        """Initialize and add all tabs to the tab view."""
        self.recon_tab = ReconTab(self.tab_view.add("Recon"))
        self.brute_tab = BruteTab(self.tab_view.add("Brute Force"))
        self.exploit_tab = ExploitsTab(self.tab_view.add("Exploits"))
        self.reports_tab = ReportsTab(self.tab_view.add("Reports"))
        self.ids_tab = IDSTab(self.tab_view.add("IDS"))
        self.auto_mode_tab = AutoModeTab(self.tab_view.add("Auto Mode"))
        self.settings_tab = SettingsTab(self.tab_view.add("Settings"))

if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()