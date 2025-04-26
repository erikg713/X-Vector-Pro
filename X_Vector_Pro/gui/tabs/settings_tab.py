import customtkinter as ctk
from tkinter import filedialog
from utils.settings import save_settings
from utils.logger import log_to_central

def load_settings_tab(tab, settings):
    def browse_default_wordlist():
        path = filedialog.askopenfilename()
        if path:
            wordlist_path_entry.delete(0, "end")
            wordlist_path_entry.insert(0, path)

    def save_settings_to_file():
        config = {
            "use_proxy": proxy_toggle.get(),
            "delay_seconds": delay_slider.get(),
            "random_user_agent": ua_toggle.get(),
            "default_wordlist": wordlist_path_entry.get().strip()
        }
        if save_settings(config):
            log_to_central("[+] Settings saved to config.json")

    # Proxy Toggle
    proxy_toggle = ctk.CTkCheckBox(tab, text="Use Proxy (future support)", onvalue=True, offvalue=False)
    proxy_toggle.pack(pady=5)
    if settings.get("use_proxy"):
        proxy_toggle.select()
    else:
        proxy_toggle.deselect()

    # Delay Slider
    ctk.CTkLabel(tab, text="Request Delay (seconds)").pack()
    delay_slider = ctk.CTkSlider(tab, from_=0.0, to=5.0, number_of_steps=50)
    delay_slider.set(settings.get("delay_seconds", 0.5))
    delay_slider.pack(pady=5)

    # User-Agent Toggle
    ua_toggle = ctk.CTkCheckBox(tab, text="Randomize User-Agent", onvalue=True, offvalue=False)
    ua_toggle.pack(pady=5)
    if settings.get("random_user_agent"):
        ua_toggle.select()
    else:
        ua_toggle.deselect()

    # Default Wordlist
    ctk.CTkLabel(tab, text="Default Wordlist Path").pack(pady=5)
    wordlist_path_entry = ctk.CTkEntry(tab, width=500)
    wordlist_path_entry.insert(0, settings.get("default_wordlist", ""))
    wordlist_path_entry.pack()

    ctk.CTkButton(tab, text="Browse", command=browse_default_wordlist).pack(pady=5)
    ctk.CTkButton(tab, text="Save Settings", command=save_settings_to_file).pack(pady=10)
