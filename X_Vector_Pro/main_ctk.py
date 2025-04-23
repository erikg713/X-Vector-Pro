import os
import json
import customtkinter as ctk from PIL
import Image from threading
import Thread from utils.toast
import ToastManager from utils.stealth
import enable_stealth_mode from utils.logger
import log_encrypted from gui.tabs.auto_tab
import AutoTab from gui.tabs.brute_tab
import BruteTab from gui.tabs.recon_tab
import ReconTab from gui.tabs.exploit_tab
import ExploitTab from gui.tabs.logs_tab
import LogsTab from gui.tabs.settings_tab
import SettingsTab

class XVectorProGUI(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro Supreme Edition") self.geometry("1100x700")

try:
        self.iconbitmap(os.path.join("assets", "icon.ico"))
    except Exception as e:
        print(f"Icon load failed: {e}")

    self.toast = ToastManager(self)
    self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
    self.sidebar = Sidebar(self, self.change_tab)
    self.main_frame = ctk.CTkFrame(self, corner_radius=0)

    self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)
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
    self.active_tab = None
    self.change_tab("AutoMode")

    if self.load_config().get("stealth_mode"):
        self.after(100, lambda: enable_stealth_mode(self.set_status, self.toast))

    self.bind("<Control-Shift-H>", self.hide_window)
    self.bind("<Control-q>", lambda e: self.destroy())
    self.bind("<Control-Tab>", lambda e: self.cycle_tabs())

def load_config(self):
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {}

def change_tab(self, tab_name):
    if self.active_tab:
        self.active_tab.grid_forget()
    self.active_tab = self.tabs[tab_name]
    self.active_tab.grid(row=0, column=0, sticky="nsew")
    self.set_status(f"{tab_name} tab loaded.")

def set_status(self, text):
    self.status_bar.configure(text=text)
    Thread(target=log_encrypted, args=(text,), daemon=True).start()

def hide_window(self, event=None):
    self.withdraw()
    self.toast.show("App hidden. Press Ctrl+Shift+H again to restore.", "info")
    self.bind("<Control-Shift-H>", self.restore_window)

def restore_window(self, event=None):
    self.deiconify()
    self.toast.show("App restored.", "success")
    self.bind("<Control-Shift-H>", self.hide_window)

def cycle_tabs(self):
    keys = list(self.tabs.keys())
    current = keys.index(self.active_tab.__class__.__name__.replace("Tab", ""))
    next_tab = keys[(current + 1) % len(keys)]
    self.change_tab(next_tab)

class Sidebar(ctk.CTkFrame): def init(self, parent, callback): super().init(parent, width=180, corner_radius=0) self.callback = callback self.icons = self.load_icons()

for name in ["AutoMode", "Brute", "Recon", "Exploits", "Logs", "Settings"]:
        btn = ctk.CTkButton(self, text=name, image=self.icons.get(name), anchor="w",
                            command=lambda n=name: callback(n))
        btn.pack(fill="x", padx=10, pady=5)

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
                print(f"Failed to load icon for {name}: {e}")
    return icons

if name == "main": app = XVectorProGUI() app.mainloop()

