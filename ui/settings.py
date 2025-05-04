import customtkinter as ctk
from tkinter import filedialog
from utils.settings import save_settings
from utils.logger import log_to_central

def load_settings_tab(tab_container, settings):
    settings_tab = ctk.CTkFrame(tab_container)
    tab_container.add(settings_tab, text="Settings")
    
    # Proxy Toggle
    proxy_toggle = ctk.CTkCheckBox(settings_tab, text="Use Proxy (future support)", onvalue=True, offvalue=False)
    proxy_toggle.pack(pady=5)
    proxy_toggle.select() if settings.get("use_proxy") else proxy_toggle.deselect()

    # Delay Slider
    ctk.CTkLabel(settings_tab, text="Request Delay (seconds)").pack()
    delay_slider = ctk.CTkSlider(settings_tab, from_=0.0, to=5.0, number_of_steps=50)
    delay_slider.set(settings.get("delay_seconds", 0.5))
    delay_slider.pack(pady=5)

    # User-Agent Toggle
    ua_toggle = ctk.CTkCheckBox(settings_tab, text="Randomize User-Agent", onvalue=True, offvalue=False)
    ua_toggle.pack(pady=5)
    ua_toggle.select() if settings.get("random_user_agent") else ua_toggle.deselect()

    # Default Wordlist
    ctk.CTkLabel(settings_tab, text="Default Wordlist Path").pack(pady=5)
    wordlist_path_entry = ctk.CTkEntry(settings_tab, width=500)
    wordlist_path_entry.insert(0, settings.get("default_wordlist", ""))
    wordlist_path_entry.pack()

    def browse_default_wordlist():
        path = filedialog.askopenfilename()
        if path:
            wordlist_path_entry.delete(0, "end")
            wordlist_path_entry.insert(0, path)

    ctk.CTkButton(settings_tab, text="Browse", command=browse_default_wordlist).pack(pady=5)
    ctk.CTkButton(settings_tab, text="Save Settings", command=lambda: save_settings({
        "use_proxy": proxy_toggle.get(),
        "delay_seconds": delay_slider.get(),
        "random_user_agent": ua_toggle.get(),
        "default_wordlist": wordlist_path_entry.get().strip()
    })).pack(pady=10)
