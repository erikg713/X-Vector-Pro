import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

class XVectorPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro :: WordPress Brute Force GUI")
        self.geometry("720x480")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)

        # Tabs
        self.brute_tab = ttk.Frame(tabControl)
        self.settings_tab = ttk.Frame(tabControl)
        self.log_tab = ttk.Frame(tabControl)

        tabControl.add(self.brute_tab, text='Brute Force')
        tabControl.add(self.settings_tab, text='Settings')
        tabControl.add(self.log_tab, text='Logs')
        tabControl.pack(expand=1, fill="both")

        self.setup_brute_tab()
        self.setup_settings_tab()
        self.setup_log_tab()

    def setup_brute_tab(self):
        ttk.Label(self.brute_tab, text="Target URL (xmlrpc.php):").pack(pady=5)
        self.target_entry = ttk.Entry(self.brute_tab, width=50)
        self.target_entry.pack(pady=5)

        ttk.Label(self.brute_tab, text="Username(s):").pack(pady=5)
        self.user_entry = ttk.Entry(self.brute_tab, width=50)
        self.user_entry.pack(pady=5)

        ttk.Label(self.brute_tab, text="Wordlist Path:").pack(pady=5)
        self.wordlist_entry = ttk.Entry(self.brute_tab, width=50)
        self.wordlist_entry.pack(pady=5)

        ttk.Button(self.brute_tab, text="Start Attack", command=self.start_attack).pack(pady=20)

    def setup_settings_tab(self):
        ttk.Label(self.settings_tab, text="Configuration will go here").pack(pady=10)

    def setup_log_tab(self):
        ttk.Label(self.log_tab, text="Log Output").pack()
        self.log_output = tk.Text(self.log_tab, height=20, width=80)
        self.log_output.pack()

    def log(self, msg):
        self.log_output.insert(tk.END, msg + "\n")
        self.log_output.see(tk.END)

    def start_attack(self):
        url = self.target_entry.get()
        users = self.user_entry.get().split(',')
        wordlist = self.wordlist_entry.get()

        if not os.path.isfile(wordlist):
            messagebox.showerror("Error", "Invalid wordlist path")
            return

        self.log("[+] Starting brute force on: " + url)
        self.log("[*] Using users: " + ', '.join(users))
        self.log("[*] Wordlist: " + wordlist)

        # Placeholder logic -- connect to real engine
        self.log("[!] Attack simulated. Add backend engine.")

if __name__ == '__main__':
    app = XVectorPro()
    app.mainloop()
from utils.logger import log_to_central
from utils.settings import load_settings
from utils.splash import show_splash_screen
from core.recon.recon_engine import ReconEngine
from gui.dashboard import ReconViewer
from ui.tabs import init_tabs

class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro | Silent. Adaptive. Lethal.")
        self.geometry("1024x700")

        # Appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Show splash
        show_splash_screen()

        # Recon Viewer
        self.recon_viewer = ReconViewer(self)
        self.recon_viewer.pack(fill="both", expand=True)

        # Tab view
        self.tabs = ctk.CTkTabview(self, width=980, height=620)
        self.tabs.pack(padx=10, pady=10)

        # Load settings and initialize UI tabs
        settings = load_settings()
        init_tabs(self.tabs, self, settings)

def launch_gui():
    app = XVectorGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()
