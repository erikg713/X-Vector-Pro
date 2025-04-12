import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading, json, os
from utils.logger import log_to_central
from ui.tabs import init_tabs
from utils.settings import load_settings
from utils.splash import show_splash_screen

# === Setup ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
print("7. View Auto Recon Reports")
app = ctk.CTk()
app.geometry("900x650")
app.title("X-Vector Pro | Silent. Adaptive. Lethal.")
elif choice == "7":
    import subprocess
    subprocess.Popen(["python", "gui/recon_viewer.py"])
# Splash screen
show_splash_screen()

# Initialize tab layout
tabs = ctk.CTkTabview(app, width=880, height=620)
tabs.pack(padx=10, pady=10)

# Load all tabs & sections
settings = load_settings()
init_tabs(tabs, app, settings)

# Run the GUI app
app.mainloop()
from gui.dashboard import launch_gui

if __name__ == "__main__":
    launch_gui()
