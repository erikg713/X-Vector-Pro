import customtkinter as ctk from gui.tabs import init_tabs from utils.splash import show_splash_screen from utils.settings import load_settings

class XVectorGUI(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro | Silent. Adaptive. Lethal.") self.geometry("1024x700")

# Appearance settings
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Splash screen
    show_splash_screen()

    # Main tab view
    self.tabs = ctk.CTkTabview(self, width=980, height=640)
    self.tabs.pack(padx=10, pady=10)

    # Load settings and init tabs
    settings = load_settings()
    init_tabs(self.tabs, self)

def launch_gui(): app = XVectorGUI() app.mainloop()

if name == "main": launch_gui()

