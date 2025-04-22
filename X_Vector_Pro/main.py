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
import customtkinter as ctk
from PIL import Image
import os
import random
import time
import requests
import json
from queue import Queue
import threading

class XVectorProGUI(ctk.CTk): 
    def __init__(self): 
        super().__init__()
        self.title("X-Vector Pro Supreme Edition")
        self.geometry("1100x700")
        self.iconbitmap("assets/icon.ico") if os.path.exists("assets/icon.ico") else None

        # Sidebar
        self.sidebar = Sidebar(self, self.change_tab)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)

        # Toast System
        self.toast = ToastManager(self)

        # Tab system
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

        # Load configuration
        config = self.load_config()
        if config.get("stealth_mode"):
            self.after(100, lambda: enable_stealth_mode(self.set_status, self.toast))

        # Hotkeys for hiding/restoring the app
        self.bind("<Control-Shift-H>", self.hide_window)

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

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except:
            return {}

class Sidebar(ctk.CTkFrame): 
    def __init__(self, parent, callback): 
        super().__init__(parent, width=180, corner_radius=0)
        self.callback = callback
        self.icons = self.load_icons()
        
        # Sidebar Buttons
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

class ToastManager:
    def __init__(self, parent):
        self.parent = parent
        self.toast_label = ctk.CTkLabel(parent, text="", fg_color="yellow", width=250, height=40)
        self.toast_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.toast_label.grid_forget()

    def show(self, message, type="info"):
        colors = {"info": "blue", "error": "red", "success": "green"}
        self.toast_label.configure(text=message, fg_color=colors.get(type, "blue"))
        self.toast_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.parent.after(3000, self.hide)

    def hide(self):
        self.toast_label.grid_forget()

def stealth_delay(min_ms=200, max_ms=800):
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

def stealth_headers():
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        ]),
        "Accept-Language": "en-US,en;q=0.9",
    }
    return headers

def scan_path(path, url):
    full_url = f"{url}/{path}"
    try:
        stealth_delay(300, 1200)
        r = requests.get(full_url, headers=stealth_headers(), timeout=5)
        if r.status_code in [200, 301, 403]:
            line = f"[+] {full_url} [{r.status_code}]"
            scanner_output.insert("end", line + "\n")
            log_to_file("dirscan", line)
    except Exception as e:
        pass

def run_dir_scan(url):
    if not url.startswith("http"):
        show_toast("Use full URL (http/https).", "error")
        return
    
    scanner_output.insert("end", "\n[*] Starting directory scan...\n")
    log_to_file("dirscan", f"Scanning started on {url}")
    
    wordlist = ["admin", "login", "dashboard", "config", "backup", "wp-admin", "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"]
    queue = Queue()

    # Define worker threads
    def worker():
        while not queue.empty():
            path = queue.get()
            scan_path(path, url)
            queue.task_done()

    # Add items to queue
    for path in wordlist:
        queue.put(path)

    # Launch threads
    threads = []
    for _ in range(5):  # Use 5 threads for concurrent scanning
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    show_toast("Dir scan complete", "success")
    scanner_output.insert("end", "[*] Dir scan finished.\n")

def show_toast(message, type="info"):
    app.toast.show(message, type)

if __name__ == "__main__":
    app = XVectorProGUI()
    app.mainloop()
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
    # Directory scan using threading
def scan_path_threaded(path, url, queue, scanner_output):
    try:
        stealth_delay(300, 1200)
        full_url = f"{url}/{path}"
        r = requests.get(full_url, headers=stealth_headers(), timeout=5)
        if r.status_code in [200, 301, 403]:
            line = f"[+] {full_url} [{r.status_code}]"
            queue.put(line)  # Add result to queue for UI update
    except Exception as e:
        pass

def worker_thread(queue, threads_done, scanner_output):
    while not queue.empty():
        path = queue.get()
        scan_path_threaded(path, scanner_output.url, queue, scanner_output)
        queue.task_done()

    threads_done.append(True)  # Indicate completion of thread task

def start_scan(url):
    scanner_output.insert("end", "[*] Starting directory scan...\n")
    log_to_file("dirscan", f"Started scanning {url}")
    
    wordlist = ["admin", "login", "dashboard", "config", "backup", "wp-admin", "uploads", "includes", "panel", "cpanel", "private", "hidden", "db", "phpmyadmin"]
    queue = Queue()

    # Populate queue with paths
    for path in wordlist:
        queue.put(path)

    threads_done = []

    # Launch multiple threads for scanning
    threads = []
    for _ in range(5):  # Adjust the number of threads based on your needs
        t = threading.Thread(target=worker_thread, args=(queue, threads_done, scanner_output))
        threads.append(t)
        t.start()

    # Wait for threads to finish
    for t in threads:
        t.join()

    # Check if all threads are done
    if len(threads_done) == len(threads):
        scanner_output.insert("end", "[*] Directory scan completed.\n")
        show_toast("Dir scan complete", "success")
        from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
def generate_key():
    return Fernet.generate_key()

# Encrypt a message
def encrypt_message(message, key):
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

# Decrypt a message
def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message

# Log to file with encryption
def log_to_file(filename, message, key=None):
    log_dir = "logs/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if key is None:
        key = generate_key()

    encrypted_message = encrypt_message(message, key)

    log_path = os.path.join(log_dir, f"{filename}.log")
    with open(log_path, "ab") as f:
        f.write(encrypted_message + b'\n')
    
    return key

# Example of decrypting the logs
def read_encrypted_log(filename, key):
    log_dir = "logs/"
    log_path = os.path.join(log_dir, f"{filename}.log")

    with open(log_path, "rb") as f:
        encrypted_logs = f.readlines()

    decrypted_logs = []
    for encrypted_log in encrypted_logs:
        decrypted_logs.append(decrypt_message(encrypted_log.strip(), key))

    return decrypted_logs

if __name__ == "__main__":
    app = XVectorProGUI()
    app.mainloop()
