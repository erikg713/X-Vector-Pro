import os
import logging
import customtkinter as ctk
from gui.tabs.recon_tab import ReconTab
from gui.tabs.brute_tab import BruteTab
from gui.tabs.exploit_tab import ExploitsTab
from gui.tabs.reports_tab import ReportsTab
from gui.tabs.ids_tab import IDSTab
from gui.tabs.auto_mode_tab import AutoModeTab
from gui.tabs.settings_tab import SettingsTab
from gui.tabs.cve_tab import CVETab
from gui.tabs.logs_tab import load_logs_tab

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

        # Add tabs dynamically
        self.add_tabs()

    def configure_gui(self):
        """Configure the GUI settings such as appearance and theme."""
        default_appearance = "dark"
        default_theme = "blue"

        # Check for config file (optional future support)
        if os.path.exists("config.json"):
            import json
            try:
                with open("config.json", "r") as config_file:
                    config = json.load(config_file)
                    appearance = config.get("appearance", default_appearance)
                    theme = config.get("theme", default_theme)
            except Exception as e:
                logging.error(f"Error loading configuration file: {e}")
                appearance, theme = default_appearance, default_theme
        else:
            appearance, theme = default_appearance, default_theme

        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(theme)
        logging.info(f"GUI configured with appearance: {appearance}, theme: {theme}")

    def get_window_geometry(self):
        """Return appropriate window geometry based on screen size."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        return f"{window_width}x{window_height}"

    def add_tabs(self):
        """Initialize and add all tabs to the tab view."""
        tab_classes = {
            "Recon": ReconTab,
            "Brute Force": BruteTab,
            "Exploits": ExploitsTab,
            "Reports": ReportsTab,
            "IDS": IDSTab,
            "Auto Mode": AutoModeTab,
            "Settings": SettingsTab,
            "CVE Lookup": CVETab,
            "Logs": load_logs_tab  # Special loader function
        }

        self.tabs = {}  # Dictionary to store tab instances
        for tab_name, TabClass in tab_classes.items():
            try:
                if callable(TabClass):  # Check if it's a loader function
                    tab = self.tab_view.add(tab_name)
                    TabClass(tab)  # Call the loader function
                else:
                    self.tabs[tab_name] = TabClass(self.tab_view.add(tab_name))
                logging.info(f"Successfully added tab: {tab_name}")
            except Exception as e:
                logging.error(f"Error initializing tab '{tab_name}': {e}")
                error_tab = self.tab_view.add(tab_name)
                error_label = ctk.CTkLabel(error_tab, text=f"Error loading {tab_name} tab", text_color="red")
                error_label.pack(pady=20)

if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
