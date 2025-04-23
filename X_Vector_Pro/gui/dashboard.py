import sys
import os
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

class Toast(ctk.CTkToplevel):
    def __init__(self, master, message, duration=2000):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(fg_color="#2e2e2e")
        self.geometry(f"250x40+{master.winfo_x() + 50}+{master.winfo_y() + 50}")
        label = ctk.CTkLabel(self, text=message, text_color="white")
        label.pack(padx=10, pady=5)
        self.after(duration, self.destroy)

def show_toast(master, message):
    Toast(master, message)

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1200x800")
        self.minsize(1024, 700)

        self.active_tab = None
        self.tab_instances = {}

        self.build_sidebar()
        self.build_main_area()

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="X-Vector Pro", font=("Arial", 20, "bold")).pack(pady=20)

        for tab_name in TAB_CLASSES:
            ctk.CTkButton(
                self.sidebar,
                text=tab_name,
                command=lambda name=tab_name: self.switch_tab(name)
            ).pack(padx=10, pady=5, fill="x")

    def build_main_area(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", expand=True, fill="both")

    def switch_tab(self, tab_name):
        if self.active_tab:
            self.active_tab.pack_forget()

        if tab_name not in self.tab_instances:
            self.tab_instances[tab_name] = TAB_CLASSES[tab_name](self.content_frame)

        self.active_tab = self.tab_instances[tab_name]
        self.active_tab.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
