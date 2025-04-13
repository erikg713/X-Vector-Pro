import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading, json, os
from utils.logger import log_to_central
from ui.tabs import init_tabs
from utils.settings import load_settings
from utils.splash import show_splash_screen
from gui.dashboard import ReconViewer
import customtkinter as ctk
from core.recon.recon_engine import ReconEngine
class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1024x700")

        self.recon_viewer = ReconViewer(self)
        self.recon_viewer.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = XVectorGUI()
    app.mainloop()
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
