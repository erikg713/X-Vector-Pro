import os
import time
import random
import json
import threading
from queue import Queue
from datetime import datetime
from tkinter import messagebox, filedialog
import customtkinter as ctk
import requests
import xmlrpc.client
import tldextract
from PIL import Image
from utils.toast import ToastManager
from utils.stealth import enable_stealth_mode, stealth_delay
from utils.logger import log_encrypted
from gui.tabs.auto_tab import AutoTab
from gui.tabs.brute_tab import BruteTab
from gui.tabs.recon_tab import ReconTab
from gui.tabs.exploit_tab import ExploitTab
from gui.tabs.logs_tab import LogsTab
from gui.tabs.settings_tab import SettingsTab
from utils.proxy import get_proxy
import os, time, socket, json, random, threading, requests, xmlrpc.client from queue import Queue from datetime import datetime from urllib.parse import urljoin from tkinter import messagebox, filedialog import customtkinter as ctk from PIL import Image import tldextract

from utils.toast import ToastManager from utils.stealth import enable_stealth_mode from utils.logger import log_encrypted

from gui.tabs.auto_tab import AutoTab from gui.tabs.brute_tab import BruteTab from gui.tabs.recon_tab import ReconTab from gui.tabs.exploit_tab import ExploitTab from gui.tabs.logs_tab import LogsTab from gui.tabs.settings_tab import SettingsTab

ctk.set_appearance_mode("dark") ctk.set_default_color_theme("dark-blue")

class XVectorProGUI(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro Supreme Edition") self.geometry("1100x700") self.iconbitmap("assets/icon.ico") if os.path.exists("assets/icon.ico") else None

self.sidebar = Sidebar(self, self.change_tab)
    self.sidebar.grid(row=0, column=0, sticky="ns")

    self.main_frame = ctk.CTkFrame(self, corner_radius=0)
    self.main_frame.grid(row=0, column=1, sticky="nsew")

    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
    self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)

    self.toast = ToastManager(self)

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

    config = self.load_config()
    if config.get("stealth_mode"):
        self.after(100, lambda: enable_stealth_mode(self.set_status, self.toast))

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


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class XVectorProGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro Supreme Edition")
        self.geometry("1100x700")
        self.iconbitmap("assets/icon.ico") if os.path.exists("assets/icon.ico") else None

        self.sidebar = Sidebar(self, self.change_tab)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)

        self.toast = ToastManager(self)

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

        config = self.load_config()
        if config.get("stealth_mode"):
            self.after(100, lambda: enable_stealth_mode(self.set_status, self.toast))

        self.bind("<Control-Shift-H>", self.hide_window)

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

    def hide_window(self, event=None):
        self.withdraw()
        self.toast.show("App hidden. Press Ctrl+Shift+H again to restore.", "info")
        self.bind("<Control-Shift-H>", self.restore_window)

    def restore_window(self, event=None):
        self.deiconify()
        self.toast.show("App restored.", "success")
        self.bind("<Control-Shift-H>", self.hide_window)

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, width=180, corner_radius=0)
        self.callback = callback
        self.icons = self.load_icons()
        
        buttons = [
            ("AutoMode", self.icons.get("AutoMode")),
            ("Brute", self.icons.get("Brute")),
            ("Recon", self.icons.get("Recon")),
            ("Exploits", self.icons.get("Exploits")),
            ("Logs", self.icons.get("Logs")),
            ("Settings", self.icons.get("Settings")),
        ]
        
        for name, icon in buttons:
            btn = ctk.CTkButton(self, text=name, image=icon, anchor="w", command=lambda n=name: callback(n))
            btn.pack(fill="x", padx=10, pady=5)

    def load_icons(self):
        icon_dir = "assets/icons/"
        icons = {}
        for name in ["AutoMode", "Brute", "Recon", "Exploits", "Logs", "Settings"]:
            path = os.path.join(icon_dir, f"{name.lower()}.png")
            if os.path.exists(path):
                img = ctk.CTkImage(Image.open(path).resize((20, 20)))
                icons[name] = img
        return icons

def run_dir_scan(scanner_target_entry, scanner_output):
    url = scanner_target_entry.get().strip().rstrip("/")
    if not url.startswith("http"):
        show_toast("Use full URL (http/https).", "error")
        return

    scanner_output.insert("end", "\n[*] Starting directory scan...\n")
    log_to_file("dirscan", f"Scanning started on {url}")

    wordlist = ["admin", "login", "dashboard", "config", "backup", "wp-admin", "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"]
    
    def scan_path(path):
        full_url = f"{url}/{path}"
        try:
            stealth_delay(300, 1200)
            r = requests.get(full_url, timeout=5, proxies=get_proxy())  # Implement proxy rotation
            if r.status_code in [200, 301, 403]:
                line = f"[+] {full_url} [{r.status_code}]"
                scanner_output.insert("end", line + "\n")
                log_to_file("dirscan", line)
        except Exception:
            pass
    
    threads = []
    for path in wordlist:
        t = threading.Thread(target=scan_path, args=(path,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    show_toast("Dir scan complete", "success")
    scanner_output.insert("end", "[*] Dir scan finished.\n")

def log_to_file(module, content):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"logs/{module}_{timestamp}.log", "a") as f:
        f.write(content + "\n")

def show_toast(msg, level="info"):
    color = {"info": "#2fa4ff", "error": "#ff5252", "success": "#27c93f"}.get(level, "#333")
    toast = ctk.CTkToplevel()
    toast.geometry("250x50+1050+80")
    toast.configure(bg=color)
    toast.wm_overrideredirect(True)
    label = ctk.CTkLabel(toast, text=msg, fg_color=color, text_color="white")
    label.pack(fill="both", expand=True)
    toast.after(3000, toast.destroy)

if __name__ == "__main__":
    app = XVectorProGUI()
    app.mainloop()


import os, time, socket, json, random, threading, requests, xmlrpc.client from queue import Queue from datetime import datetime from urllib.parse import urljoin from tkinter import messagebox, filedialog import customtkinter as ctk from PIL import Image import tldextract

from utils.toast import ToastManager from utils.stealth import enable_stealth_mode from utils.logger import log_encrypted

from gui.tabs.auto_tab import AutoTab from gui.tabs.brute_tab import BruteTab from gui.tabs.recon_tab import ReconTab from gui.tabs.exploit_tab import ExploitTab from gui.tabs.logs_tab import LogsTab from gui.tabs.settings_tab import SettingsTab

ctk.set_appearance_mode("dark") ctk.set_default_color_theme("dark-blue")

class XVectorProGUI(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro Supreme Edition") self.geometry("1100x700") self.iconbitmap("assets/icon.ico") if os.path.exists("assets/icon.ico") else None

self.sidebar = Sidebar(self, self.change_tab)
    self.sidebar.grid(row=0, column=0, sticky="ns")

    self.main_frame = ctk.CTkFrame(self, corner_radius=0)
    self.main_frame.grid(row=0, column=1, sticky="nsew")

    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
    self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)

    self.toast = ToastManager(self)

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

    config = self.load_config()
    if config.get("stealth_mode"):
        self.after(100, lambda: enable_stealth_mode(self.set_status, self.toast))

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

