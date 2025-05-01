import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils.settings import save_settings
from utils.logger import log_to_central
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

CONFIG_PATH = "config.json"

class SettingsTab:
    def __init__(self, parent, toast_manager):
        self.toast = toast_manager
        self.frame = ttk.Frame(parent)
        self.entries = {}
        self.checkbox_vars = {}

        self._load_config()
        self._build_ui()

    def _load_config(self):
        if not os.path.exists(CONFIG_PATH):
            self.config = {}
            self.toast.show("Warning: config.json not found.")
        else:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)

    def _build_ui(self):
        ttk.Label(self.frame, text="X-Vector Settings", font=("Segoe UI", 14, "bold")).pack(pady=10)

        form = ttk.Frame(self.frame)
        form.pack(pady=10, padx=15)

        # Boolean flags
        self._add_checkbox(form, "stealth_mode", "Enable Stealth Mode")
        self._add_checkbox(form, "use_proxy", "Use Proxy List")
        self._add_checkbox(form, "use_tor", "Use Tor for Traffic")
        self._add_checkbox(form, "random_user_agent", "Randomize User-Agent")

        # Standard entries
        self._add_entry(form, "smtp_server", "SMTP Server")
        self._add_entry(form, "smtp_port", "SMTP Port")
        self._add_entry(form, "smtp_user", "SMTP Username")
        self._add_entry(form, "smtp_pass", "SMTP Password", show="*")
        self._add_entry(form, "proxy_list", "Proxy List (comma-separated)")
        self._add_entry(form, "delay_seconds", "Fixed Delay (sec)")
        self._add_entry(form, "random_delay_min", "Random Delay Min")
        self._add_entry(form, "random_delay_max", "Random Delay Max")
        self._add_entry(form, "concurrency", "Max Concurrency")
        self._add_entry(form, "retry_delay", "Retry Delay (sec)")
        self._add_entry(form, "default_wordlist", "Default Wordlist Path", button="Browse")

        # Save button
        ttk.Button(self.frame, text="Save Configuration", command=self._save_config).pack(pady=15)

    def _add_checkbox(self, parent, key, label):
        var = tk.BooleanVar(value=self.config.get(key, False))
        cb = ttk.Checkbutton(parent, text=label, variable=var)
        cb.pack(anchor="w", pady=2)
        self.checkbox_vars[key] = var

    def _add_entry(self, parent, key, label, show=None, button=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=3)

        ttk.Label(frame, text=label, width=22).pack(side="left")

        entry_var = tk.StringVar(value=str(self.config.get(key, "")))
        entry = ttk.Entry(frame, textvariable=entry_var, show=show, width=50)
        entry.pack(side="left", padx=5)

        if button == "Browse":
            ttk.Button(frame, text="...", width=3, command=lambda: self._browse_file(entry_var)).pack(side="left")

        self.entries[key] = entry_var

    def _browse_file(self, var):
        path = filedialog.askopenfilename(initialdir="wordlists/", filetypes=[("Text files", "*.txt")])
        if path:
            var.set(path)

    def _save_config(self):
        for key, var in self.entries.items():
            value = var.get().strip()
            if key in ["smtp_port", "delay_seconds", "random_delay_min", "random_delay_max", "concurrency", "retry_delay"]:
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    self.toast.show(f"Invalid numeric value for {key}")
                    return
            elif key == "proxy_list":
                value = [x.strip() for x in value.split(",") if x.strip()]
            self.config[key] = value

        for key, var in self.checkbox_vars.items():
            self.config[key] = var.get()

        try:
            with open(CONFIG_PATH, "w") as f:
                json.dump(self.config, f, indent=2)
            self.toast.show("Settings saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
def load_settings_tab(tab, settings):
    # Function to browse and select the wordlist path
    def browse_default_wordlist():
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            wordlist_path_entry.delete(0, "end")
            wordlist_path_entry.insert(0, path)

    # Function to save the settings to a config file
    def save_settings_to_file():
        # Validate wordlist path
        wordlist_path = wordlist_path_entry.get().strip()
        if wordlist_path and not wordlist_path.endswith(".txt"):
            messagebox.showerror("Invalid Path", "Please select a valid text file (.txt) for the wordlist.")
            return
        
        # Construct configuration dictionary
        config = {
            "use_proxy": proxy_toggle.get(),
            "delay_seconds": delay_slider.get(),
            "random_user_agent": ua_toggle.get(),
            "default_wordlist": wordlist_path
        }

        # Save settings and provide feedback
        if save_settings(config):
            log_to_central("[+] Settings saved to config.json")
            messagebox.showinfo("Settings Saved", "Settings have been successfully saved.")
        else:
            messagebox.showerror("Error", "Failed to save settings. Please try again.")

    # Proxy Toggle
    proxy_toggle = ctk.CTkCheckBox(tab, text="Use Proxy (future support)", onvalue=True, offvalue=False)
    proxy_toggle.pack(pady=5)
    proxy_toggle.select() if settings.get("use_proxy") else proxy_toggle.deselect()

    # Delay Slider
    ctk.CTkLabel(tab, text="Request Delay (seconds)").pack(pady=5)
    delay_slider = ctk.CTkSlider(tab, from_=0.0, to=5.0, number_of_steps=50)
    delay_slider.set(settings.get("delay_seconds", 0.5))
    delay_slider.pack(pady=5)

    # User-Agent Toggle
    ua_toggle = ctk.CTkCheckBox(tab, text="Randomize User-Agent", onvalue=True, offvalue=False)
    ua_toggle.pack(pady=5)
    ua_toggle.select() if settings.get("random_user_agent") else ua_toggle.deselect()

    # Default Wordlist
    ctk.CTkLabel(tab, text="Default Wordlist Path").pack(pady=5)
    wordlist_path_entry = ctk.CTkEntry(tab, width=500)
    wordlist_path_entry.insert(0, settings.get("default_wordlist", ""))
    wordlist_path_entry.pack(pady=5)

    # Browse Button
    ctk.CTkButton(tab, text="Browse", command=browse_default_wordlist).pack(pady=5)

    # Save Settings Button
    ctk.CTkButton(tab, text="Save Settings", command=save_settings_to_file).pack(pady=10)

    # Additional spacing for clarity
    ctk.CTkLabel(tab, text=" ").pack(pady=5)
