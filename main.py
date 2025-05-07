import customtkinter as ctk
import logging
import os
import json
from tkinter import filedialog, messagebox, Menu

from gui.tabs.recon_tab import ReconTab
from gui.tabs.brute_tab import BruteTab
from gui.tabs.exploit_tab import ExploitsTab
from gui.tabs.reports_tab import ReportsTab
from gui.tabs.ids_tab import IDSTab
from gui.tabs.auto_mode_tab import AutoModeTab
from gui.tabs.settings_tab import SettingsTab
from gui.tabs.cve_tab import CVETab
from gui.tabs.logs_tab import load_logs_tab

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
        self.create_menu()

        self.tab_view = ctk.CTkTabview(self, width=1280, height=960)
        self.tab_view.pack(expand=True, fill="both")
        self.add_tabs()

    def configure_gui(self):
        default_appearance = "dark"
        default_theme = "blue"
        appearance = default_appearance
        theme = default_theme

        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)
                    appearance = config.get("appearance", default_appearance)
                    theme = config.get("theme", default_theme)
        except Exception as e:
            logging.error(f"Error reading config.json: {e}")

        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(theme)

    def get_window_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width, height = 1280, 960
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        return f"{width}x{height}+{x}+{y}"

    def create_menu(self):
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Config", command=self.open_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def open_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    config = json.load(f)
                    messagebox.showinfo("Config Loaded", "Configuration loaded successfully.")
                    logging.info("Configuration loaded from: %s", file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration.\n{e}")
                logging.error("Error loading config: %s", e)

    def show_about(self):
        messagebox.showinfo("About X-Vector Pro", "X-Vector Pro\nCybersecurity Toolkit\nVersion 1.0")

    def add_tabs(self):
        ReconTab(self.tab_view.add("Recon"))
        BruteTab(self.tab_view.add("Brute"))
        ExploitsTab(self.tab_view.add("Exploits"))
        ReportsTab(self.tab_view.add("Reports"))
        IDSTab(self.tab_view.add("IDS"))
        AutoModeTab(self.tab_view.add("Auto Mode"))
        SettingsTab(self.tab_view.add("Settings"))
        CVETab(self.tab_view.add("CVEs"))
        load_logs_tab(self.tab_view.add("Logs"))

if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
