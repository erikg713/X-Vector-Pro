import customtkinter as ctk
import logging
import os
import json
from tkinter import filedialog, messagebox
from tkinter import Menu
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
        self.create_menu()

        # Create and pack the main tab view
        self.tab_view = ctk.CTkTabview(self, width=1280, height=960)
        self.tab_view.pack(expand=True, fill="both")
        self.add_tabs()

    def configure_gui(self):
        default_appearance = "dark"
        default_theme = "blue"

        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)
                    appearance = config.get("appearance", default_appearance)
                    theme = config.get("theme", default_theme)
            else:
                appearance, theme = default_appearance, default_theme
        except Exception as e:
            logging.error(f"Error reading config.json: {e}")
            appearance, theme = default_appearance, default_theme

        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(theme)
        logging.info(f"Appearance: {appearance}, Theme: {theme}")

    def create_menu(self):
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            logging.info(f"Opened file: {file_path}")
            messagebox.showinfo("File Opened", f"File opened successfully:\n{file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            logging.info(f"Saved file: {file_path}")
            messagebox.showinfo("File Saved", f"File saved successfully:\n{file_path}")

    def show_about(self):
        messagebox.showinfo("About", "X-Vector Pro - Cybersecurity Toolkit\nVersion 1.0")

    def get_window_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)
        return f"{width}x{height}"

    def add_tabs(self):
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
                tab_frame = self.tab_view.add(tab_name)
                if callable(TabClass):  # for load_logs_tab
                    TabClass(tab_frame)
                else:
                    TabClass(tab_frame)
                logging.info(f"{tab_name} tab loaded successfully.")
            except Exception as e:
                logging.error(f"Failed to load {tab_name} tab: {e}")

if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
