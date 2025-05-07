import os
import json
import time
import threading
from threading import Thread
import customtkinter as ctk
from PIL import Image

from utils.toast import ToastManager
from utils.stealth import enable_stealth_mode
from utils.logger import log_encrypted

from gui.tabs.auto_tab import AutoTab
from gui.tabs.brute_tab import BruteTab
from gui.tabs.recon_tab import ReconTab
from gui.tabs.exploit_tab import ExploitTab
from gui.tabs.logs_tab import LogsTab
from gui.tabs.settings_tab import SettingsTab


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

        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=2)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabs = {
            "AutoMode": AutoTab(self.main_frame, self.toast, self.set_status),
            "Brute": BruteTab(self.main_frame, self.toast, self.set_status),
            "Recon": ReconTab(self.main_frame, self.toast, self.set_status),
            "Exploits": ExploitTab(self.main_frame, self.toast, self.set_status),
            "Logs": LogsTab(self.main_frame, self.toast),
            "Settings": SettingsTab(self.main_frame, self.toast),
        }

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
            if os.name == "nt":
                self.iconbitmap(os.path.join("assets", "icon.ico"))
        except Exception as e:
            print(f"[Warning] Icon load failed: {e}")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                log_encrypted("[Config] Loaded configuration settings.")
                return config
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
        self.bind("<Control-Shift-Tab>", lambda e: self.cycle_tabs(reverse=True))

    def hide_window(self, event=None):
        self.withdraw()
        self.toast.show("App hidden. Press Ctrl+Shift+H to restore.", "info")
        self.bind("<Control-Shift-H>", self.restore_window)

    def restore_window(self, event=None):
        self.deiconify()
        self.toast.show("App restored.", "success")
        self.bind("<Control-Shift-H>", self.hide_window)

    def cycle_tabs(self, reverse=False):
        keys = list(self.tabs.keys())
        idx = keys.index(self.active_tab_name)
        next_idx = (idx - 1) % len(keys) if reverse else (idx + 1) % len(keys)
        self.change_tab(keys[next_idx])


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, width=180, corner_radius=0)
        self.pack_propagate(False)
        self.callback = callback
        self.buttons = {}
        self.icons = self.load_icons()
        self.create_buttons()

    def load_icons(self):
        icon_dir = os.path.join("assets", "icons")
        icons = {}
        for name in ["AutoMode", "Brute", "Recon", "Exploits", "Logs", "Settings"]:
            path = os.path.join(icon_dir, f"{name.lower()}.png")
            if os.path.exists(path):
                try:
                    img = ctk.CTkImage(Image.open(path).resize((20, 20)))
                    icons[name] = img
                except Exception as e:
                    print(f"[Warning] Failed to load icon for {name}: {e}")
        return icons

    def create_buttons(self):
        for name in ["AutoMode", "Brute", "Recon", "Exploits", "Logs", "Settings"]:
            btn = ctk.CTkButton(
                self,
                text=name,
                image=self.icons.get(name),
                anchor="w",
                command=lambda n=name: self.callback(n)
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.buttons[name] = btn

    def highlight(self, active_tab):
        for name, btn in self.buttons.items():
            btn.configure(fg_color="#2E8B57" if name == active_tab else "transparent")


if __name__ == "__main__":
    app = XVectorProGUI()
    app.mainloop()
