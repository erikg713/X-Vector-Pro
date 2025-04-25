# gui/main_ui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
import tkinter as tk
from tkinter import ttk

class XVectorPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro :: WordPress Brute Force GUI")
        self.geometry("720x480")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)

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
        self.log("[!] Attack simulated. Add backend engine.")
