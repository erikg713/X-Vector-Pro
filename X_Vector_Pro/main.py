import os, json, time, random, threading, requests from datetime import datetime from PIL import Image from tkinter import filedialog, messagebox from urllib.parse import urljoin import customtkinter as ctk

from utils.toast import ToastManager from utils.stealth import enable_stealth_mode from utils.logger import log_encrypted

from gui.tabs.auto_tab import AutoTab from gui.tabs.brute_tab import BruteTab from gui.tabs.recon_tab import ReconTab from gui.tabs.exploit_tab import ExploitTab from gui.tabs.logs_tab import LogsTab from gui.tabs.settings_tab import SettingsTab

ctk.set_appearance_mode("dark") ctk.set_default_color_theme("dark-blue")

class XVectorProGUI(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro Supreme Edition") self.geometry("1100x700") self.iconbitmap("assets/icon.ico") if os.path.exists("assets/icon.ico") else None

# Layout
    self.sidebar = Sidebar(self, self.change_tab)
    self.sidebar.grid(row=0, column=0, sticky="ns")
    self.main_frame = ctk.CTkFrame(self, corner_radius=0)
    self.main_frame.grid(row=0, column=1, sticky="nsew")
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
    self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)

    # Toasts
    self.toast = ToastManager(self)

    # Tabs
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

    # Background stealth if enabled
    config = self.load_config()
    if config.get("stealth_mode"):
        self.after(100, lambda: enable_stealth_mode(self.set_status, self.toast))

    # Keyboard shortcuts
    self.bind("<Control-r>", lambda e: self.change_tab("Recon"))

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
    log_encrypted(text)

class Sidebar(ctk.CTkFrame): def init(self, parent, callback): super().init(parent, width=180, corner_radius=0) self.callback = callback self.icons = self.load_icons() buttons = [ ("AutoMode", self.icons.get("AutoMode")), ("Brute", self.icons.get("Brute")), ("Recon", self.icons.get("Recon")), ("Exploits", self.icons.get("Exploits")), ("Logs", self.icons.get("Logs")), ("Settings", self.icons.get("Settings")), ] for name, icon in buttons: btn = ctk.CTkButton(self, text=name, image=icon, anchor="w", command=lambda n=name: callback(n)) btn.pack(fill="x", padx=10, pady=5)

def load_icons(self):
    icon_dir = "assets/icons/"
    icons = {}
    for name in ["AutoMode", "Brute", "Recon", "Exploits", "Logs", "Settings"]:
        path = os.path.join(icon_dir, f"{name.lower()}.png")
        if os.path.exists(path):
            img = ctk.CTkImage(Image.open(path).resize((20, 20)))
            icons[name] = img
    return icons

if name == "main": app = XVectorProGUI() app.mainloop()

