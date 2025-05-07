import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils.settings import save_settings
from utils.logger import log_to_central

def browse_default_wordlist(entry):
    path = filedialog.askopenfilename(
        title="Select Default Wordlist",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if path:
        entry.delete(0, "end")
        entry.insert(0, path)

def save_settings_to_file(proxy_toggle, delay_slider, ua_toggle, wordlist_path_entry):
    config = {
        "use_proxy": proxy_toggle.get(),
        "delay_seconds": delay_slider.get(),
        "random_user_agent": ua_toggle.get(),
        "default_wordlist": wordlist_path_entry.get().strip()
    }
    if save_settings(config):
        log_to_central("[+] Settings saved to config.json")
        messagebox.showinfo("Success", "Settings saved successfully!")
    else:
        messagebox.showerror("Error", "Failed to save settings.")

def load_settings_tab(tab, settings):
    # General container
    container = ctk.CTkFrame(tab)
    container.pack(pady=10, padx=10, fill="both", expand=True)

    # --- Proxy Section ---
    proxy_frame = ctk.CTkFrame(container)
    proxy_frame.pack(pady=10, fill="x")

    proxy_toggle = ctk.CTkCheckBox(proxy_frame, text="Use Proxy (future support)", onvalue=True, offvalue=False)
    proxy_toggle.pack(anchor="w", padx=10)
    if settings.get("use_proxy", False):
        proxy_toggle.select()
    else:
        proxy_toggle.deselect()

    # --- Delay Section ---
    delay_frame = ctk.CTkFrame(container)
    delay_frame.pack(pady=10, fill="x")

    ctk.CTkLabel(delay_frame, text="Request Delay (seconds)").pack(anchor="w", padx=10)
    delay_slider = ctk.CTkSlider(delay_frame, from_=0.0, to=5.0, number_of_steps=50)
    delay_slider.set(settings.get("delay_seconds", 0.5))
    delay_slider.pack(padx=10)

    # --- User-Agent Section ---
    ua_frame = ctk.CTkFrame(container)
    ua_frame.pack(pady=10, fill="x")

    ua_toggle = ctk.CTkCheckBox(ua_frame, text="Randomize User-Agent", onvalue=True, offvalue=False)
    ua_toggle.pack(anchor="w", padx=10)
    if settings.get("random_user_agent", False):
        ua_toggle.select()
    else:
        ua_toggle.deselect()

    # --- Wordlist Section ---
    wordlist_frame = ctk.CTkFrame(container)
    wordlist_frame.pack(pady=10, fill="x")

    ctk.CTkLabel(wordlist_frame, text="Default Wordlist Path").pack(anchor="w", padx=10, pady=(0, 5))
    wordlist_path_entry = ctk.CTkEntry(wordlist_frame, width=500)
    wordlist_path_entry.insert(0, settings.get("default_wordlist", ""))
    wordlist_path_entry.pack(side="left", padx=(10, 5), fill="x", expand=True)

    ctk.CTkButton(wordlist_frame, text="Browse", command=lambda: browse_default_wordlist(wordlist_path_entry)).pack(side="left", padx=5)

    # --- Save Button ---
    ctk.CTkButton(container, text="Save Settings", command=lambda: save_settings_to_file(
        proxy_toggle, delay_slider, ua_toggle, wordlist_path_entry)
    ).pack(pady=20)
