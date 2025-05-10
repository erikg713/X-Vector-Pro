import os
import json
import time
import threading
import customtkinter as ctk
from PIL import Image
from threading import Thread
import customtkinter as ctk from gui.tabs import init_tabs from utils.splash import show_splash_screen from utils.settings import load_settings

class XVectorGUI(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro | Silent. Adaptive. Lethal.") self.geometry("1024x700")

# Appearance settings
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Splash screen
    show_splash_screen()

    # Main tab view
    self.tabs = ctk.CTkTabview(self, width=980, height=640)
    self.tabs.pack(padx=10, pady=10)

    # Load settings and init tabs
    settings = load_settings()
    init_tabs(self.tabs, self)

def launch_gui(): app = XVectorGUI() app.mainloop()

if name == "main": launch_gui()


# Example imports - make sure they exist and are implemented
from utils.toast import ToastManager
from utils.stealth import enable_stealth_mode
from utils.logger import log_encrypted

# Ensure these imports work with valid file paths
try:
    from gui.tabs.auto_tab import AutoTab
    from gui.tabs.brute_tab import BruteTab
    from gui.tabs.recon_tab import ReconTab
    from gui.tabs.exploit_tab import ExploitTab
    from gui.tabs.logs_tab import LogsTab
    from gui.tabs.settings_tab import SettingsTab
    from gui.training_tab import TrainingTab
except ImportError as e:
    print(f"Error importing tabs: {e}")

class XVectorProGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro Supreme Edition")
        self.geometry("1100x700")
        self.resizable(False, False)

        self.stealth_intro()
        self.setup_icon()
        self.toast = ToastManager(self)

        self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.sidebar = Sidebar(self, self.change_tab)
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)

        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize tabs only if their respective classes are imported correctly
        self.tabs = {}
        try:
            self.tabs = {
                "AutoMode": AutoTab(self.main_frame, self.toast, self.set_status),
                "Brute": BruteTab(self.main_frame, self.toast, self.set_status),
                "Recon": ReconTab(self.main_frame, self.toast, self.set_status),
                "Exploits": ExploitTab(self.main_frame, self.toast, self.set_status),
                "Logs": LogsTab(self.main_frame, self.toast),
                "Settings": SettingsTab(self.main_frame, self.toast),
            }
        except Exception as e:
            print(f"Error initializing tabs: {e}")

        self.active_tab_name = None
        self.change_tab("AutoMode")

        if self.load_config().get("stealth_mode"):
            self.after(500, lambda: enable_stealth_mode(self.set_status, self.toast))

        self.bind_shortcuts()

    def stealth_intro(self):
        splash = ctk.CTkToplevel(self)
        splash.geometry("1100x700")
        splash.overrideredirect(True)
        splash.configure(fg_color="black")

        label = ctk.CTkLabel(splash, text="", text_color="lime", font=("Courier", 18))
        label.place(relx=0.5, rely=0.5, anchor="center")

        def animate_typing():
            intro_text = "Initializing X-Vector Pro Supreme Edition..."
            typed = ""
            for char in intro_text:
                typed += char
                label.configure(text=typed)
                splash.update()
                time.sleep(0.04)
            time.sleep(1.2)
            splash.destroy()

        threading.Thread(target=animate_typing, daemon=True).start()

    def setup_icon(self):
        try:
            self.iconbitmap(os.path.join("assets", "icon.ico"))
        except Exception as e:
            print(f"[Warning] Icon load failed: {e}")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] Failed to load config: {e}")
            return {}

    def change_tab(self, tab_name):
        if self.active_tab_name:
            self.tabs[self.active_tab_name].grid_forget()

        self.active_tab_name = tab_name
        tab = self.tabs[tab_name]
        tab.grid(row=0, column=0, sticky="nsew")
        self.sidebar.highlight(tab_name)
        self.set_status(f"{tab_name} tab loaded.")

    def set_status(self, text):
        self.status_bar.configure(text=text)
        Thread(target=log_encrypted, args=(text,), daemon=True).start()

    def bind_shortcuts(self):
        self.bind("<Control-Shift-H>", self.hide_window)
        self.bind("<Control-q>", lambda e: self.destroy())
        self.bind("<Control-Tab>", lambda e: self.cycle_tabs())

    def hide_window(self, event=None):
        self.withdraw()
        self.toast.show("App hidden. Press Ctrl+Shift+H to restore.", "info")
        self.bind("<Control-Shift-H>", self.restore_window)

    def restore_window(self, event=None):
        self.deiconify()
        self.toast.show("App restored.", "success")
        self.bind("<Control-Shift-H>", self.hide_window)

    def cycle_tabs(self):
        keys = list(self.tabs.keys())
        current_idx = keys.index(self.active_tab_name)
        next_idx = (current_idx + 1) % len(keys)
        self.change_tab(keys[next_idx])

# Sidebar and other components remain unchanged

if __name__ == "__main__":
    app = XVectorProGUI()
    app.mainloop()
