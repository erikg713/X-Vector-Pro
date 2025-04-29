import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils.settings import save_settings
from utils.logger import log_to_central

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
