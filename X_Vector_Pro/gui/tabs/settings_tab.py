ui/tabs_settings.py

import customtkinter as ctk from tkinter
import filedialog from utils.settings
import save_settings from utils.logger
import log_to_central

def load_settings_tab(tab, settings): def browse_default_wordlist(): path = filedialog.askopenfilename() if path: wordlist_path_entry.delete(0, "end") wordlist_path_entry.insert(0, path)

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
proxy_toggle.select() if settings.get("use_proxy") else proxy_toggle.deselect()

# Delay Slider
ctk.CTkLabel(tab, text="Request Delay (seconds)").pack()
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
wordlist_path_entry.pack()

ctk.CTkButton(tab, text="Browse", command=browse_default_wordlist).pack(pady=5)
ctk.CTkButton(tab, text="Save Settings", command=save_settings_to_file).pack(pady=10)


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QTextEdit
from core.settings import (
    load_settings,
    save_settings,
    toggle_stealth_mode,
    get_settings_summary
)

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.stealth_checkbox = QCheckBox("Enable Stealth Mode")
        self.save_button = QPushButton("Save Settings")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.stealth_checkbox)
        layout.addWidget(self.save_button)
        layout.addWidget(self.output)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.handle_save)

    def load_current_settings(self):
        try:
            config = load_settings()
            self.stealth_checkbox.setChecked(config.get("stealth_mode", False))
            self.output.setText(get_settings_summary(config))
        except Exception as e:
            self.output.setText(f"Failed to load settings: {str(e)}")

    def handle_save(self):
        stealth = self.stealth_checkbox.isChecked()
        try:
            toggle_stealth_mode(stealth)
            config = {"stealth_mode": stealth}
            save_settings(config)
            self.output.setText(get_settings_summary(config))
        except Exception as e:
            self.output.setText(f"Error saving settings: {str(e)}")
