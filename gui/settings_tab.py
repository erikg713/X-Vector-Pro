import customtkinter as ctk
from tkinter import filedialog
from utils.settings import save_settings

def settings_tab_widgets(tab, settings):
    use_proxy_toggle = ctk.CTkSwitch(tab, text="Use Proxy", onvalue=True, offvalue=False)
    use_proxy_toggle.set(settings['use_proxy'])
    use_proxy_toggle.pack(pady=10)

    delay_slider = ctk.CTkSlider(tab, from_=0, to=2, number_of_steps=10)
    delay_slider.set(settings['delay_seconds'])
    delay_slider.pack(pady=10)

    ua_toggle = ctk.CTkSwitch(tab, text="Random User Agent", onvalue=True, offvalue=False)
    ua_toggle.set(settings['random_user_agent'])
    ua_toggle.pack(pady=10)

    wordlist_path_entry = ctk.CTkEntry(tab, placeholder_text="Default Wordlist Path")
    wordlist_path_entry.insert(0, settings['default_wordlist'])
    wordlist_path_entry.pack(pady=10)

    save_button = ctk.CTkButton(tab, text="Save Settings", command=lambda: save_settings(use_proxy_toggle, delay_slider, ua_toggle, wordlist_path_entry))
    save_button.pack(pady=10)

    # You can add more settings functionality here
