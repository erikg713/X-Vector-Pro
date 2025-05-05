from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import requests
import socket
import tldextract
from datetime import datetime

# Constants
APP_TITLE = "X-Vector Pro | Silent. Adaptive. Lethal."
APP_DIMENSIONS = "900x650"
CONFIG_FILE = "config.json"
DEFAULT_SETTINGS = {
    "use_proxy": False,
    "delay_seconds": 0.5,
    "random_user_agent": True,
    "default_wordlist": "",
}
THREAD_POOL_SIZE = 10

# Utility Functions
def load_settings():
    """Load configuration settings from a JSON file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to parse the configuration file.")
    return DEFAULT_SETTINGS


def save_settings(settings):
    """Save configuration settings to a JSON file."""
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(settings, file, indent=4)
        log_message("[+] Settings saved successfully.")
    except Exception as e:
        log_message(f"[!] Error saving settings: {e}")


def log_message(message):
    """Log messages to the Logs tab."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs_output.insert("end", f"[{timestamp}] {message}\n")
    logs_output.see("end")


# GUI Setup
app = ctk.CTk()
app.title(APP_TITLE)
app.geometry(APP_DIMENSIONS)

# Tabs
tabs = ctk.CTkTabview(app, width=880, height=620)
tabs.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

settings_tab = tabs.add("Settings")
recon_tab = tabs.add("Recon")
logs_tab = tabs.add("Logs")

# Settings Tab
settings = load_settings()

def apply_settings():
    settings["use_proxy"] = proxy_toggle.get()
    settings["delay_seconds"] = delay_slider.get()
    settings["random_user_agent"] = ua_toggle.get()
    settings["default_wordlist"] = wordlist_path_entry.get().strip()
    save_settings(settings)


proxy_toggle = ctk.CTkCheckBox(settings_tab, text="Use Proxy", variable=ctk.IntVar(value=settings["use_proxy"]))
proxy_toggle.grid(row=0, column=0, sticky="w", pady=5)

ctk.CTkLabel(settings_tab, text="Request Delay (seconds)").grid(row=1, column=0, sticky="w")
delay_slider = ctk.CTkSlider(settings_tab, from_=0.0, to=5.0, number_of_steps=50)
delay_slider.set(settings["delay_seconds"])
delay_slider.grid(row=2, column=0, sticky="w", pady=5)

ua_toggle = ctk.CTkCheckBox(settings_tab, text="Randomize User-Agent", variable=ctk.IntVar(value=settings["random_user_agent"]))
ua_toggle.grid(row=3, column=0, sticky="w", pady=5)

ctk.CTkLabel(settings_tab, text="Default Wordlist Path").grid(row=4, column=0, sticky="w")
wordlist_path_entry = ctk.CTkEntry(settings_tab, width=500)
wordlist_path_entry.insert(0, settings["default_wordlist"])
wordlist_path_entry.grid(row=5, column=0, sticky="w", pady=5)

def browse_wordlist():
    file_path = filedialog.askopenfilename()
    if file_path:
        wordlist_path_entry.delete(0, "end")
        wordlist_path_entry.insert(0, file_path)

ctk.CTkButton(settings_tab, text="Browse", command=browse_wordlist).grid(row=5, column=1, sticky="w", padx=5)
ctk.CTkButton(settings_tab, text="Save Settings", command=apply_settings).grid(row=6, column=0, pady=10)

# Recon Tab
def perform_recon(target):
    recon_output.delete("0.0", "end")
    recon_output.insert("end", f"[*] Starting reconnaissance on {target}...\n")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Recon Bot)"}
        response = requests.get(target, headers=headers, timeout=10)

        # Display headers
        recon_output.insert("end", "\n--- Headers ---\n")
        for key, value in response.headers.items():
            recon_output.insert("end", f"{key}: {value}\n")

        # Detect CMS
        if "wp-content" in response.text:
            recon_output.insert("end", "[+] WordPress detected.\n")
        elif "Joomla!" in response.text:
            recon_output.insert("end", "[+] Joomla detected.\n")
        elif "Drupal" in response.text:
            recon_output.insert("end", "[+] Drupal detected.\n")
        else:
            recon_output.insert("end", "[-] No CMS detected.\n")

        # Extract domain information
        domain_info = tldextract.extract(target)
        base_domain = f"{domain_info.domain}.{domain_info.suffix}"
        ip_address = socket.gethostbyname(base_domain)
        recon_output.insert("end", f"\n[*] IP Address: {ip_address}\n")
    except Exception as e:
        recon_output.insert("end", f"[!] Recon failed: {e}\n")


def start_recon():
    target = recon_url_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Please enter a target URL.")
        return
    threading.Thread(target=perform_recon, args=(target,)).start()


ctk.CTkLabel(recon_tab, text="Target URL (e.g., https://example.com)").grid(row=0, column=0, sticky="w", pady=5)
recon_url_entry = ctk.CTkEntry(recon_tab, width=700)
recon_url_entry.grid(row=1, column=0, sticky="w", pady=5)

ctk.CTkButton(recon_tab, text="Run Recon", command=start_recon).grid(row=2, column=0, pady=10)
recon_output = ctk.CTkTextbox(recon_tab, height=400, width=800)
recon_output.grid(row=3, column=0, sticky="nsew", pady=10)

# Logs Tab
logs_output = ctk.CTkTextbox(logs_tab, height=450, width=800)
logs_output.pack(pady=10)

def clear_logs():
    logs_output.delete("0.0", "end")

ctk.CTkButton(logs_tab, text="Clear Logs", command=clear_logs).pack(pady=10)

# App Execution
app.mainloop()
