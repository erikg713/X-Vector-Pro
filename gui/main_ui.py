import customtkinter as ctk
from gui.splash_screen import show_splash_screen
from gui.brute_tab import brute_tab_widgets
from gui.logs_tab import logs_tab_widgets
from gui.settings_tab import settings_tab_widgets
from utils.logger import log_to_central
from utils.settings import load_settings, save_settings

# Show Splash Screen
show_splash_screen()

# Load settings
settings = load_settings()

# Main App Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("900x650")
app.title("X-Vector Pro | Silent. Adaptive. Lethal.")

tabs = ctk.CTkTabview(app, width=880, height=620)
tabs.pack(padx=10, pady=10)

# Add Tabs
brute_tab = tabs.add("Brute Force")
logs_tab = tabs.add("Logs")
settings_tab = tabs.add("Settings")

# Initialize Tabs
brute_tab_widgets(brute_tab)
logs_tab_widgets(logs_tab)
settings_tab_widgets(settings_tab, settings)

# Run Main Loop
app.mainloop()
