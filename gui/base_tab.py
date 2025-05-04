import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HITS_FILE = os.path.join(BASE_DIR, "logs", "hits.txt")
SESSION_FILE = os.path.join(BASE_DIR, "logs", "session.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "xvector_log.txt")
WORDLIST_DIR = os.path.join(BASE_DIR, "wordlists")

import customtkinter as ctk

class BaseTab(ctk.CTkFrame):
    def __init__(self, master, title: str = "", **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.setup_base_ui()

    def setup_base_ui(self):
        if self.title:
            ctk.CTkLabel(self, text=self.title, font=("Segoe UI", 20, "bold")).pack(pady=(10, 5))

    def add_section_label(self, text: str):
        label = ctk.CTkLabel(self, text=text, font=("Segoe UI", 14, "bold"), text_color="white")
        label.pack(anchor="w", padx=20, pady=(10, 0))
        return label

    def add_separator(self):
        separator = ctk.CTkFrame(self, height=1, fg_color="#444")
        separator.pack(fill="x", padx=20, pady=10)
        return separator

    def add_entry(self, placeholder: str = "", **kwargs):
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, **kwargs)
        entry.pack(fill="x", padx=20, pady=10)
        return entry

    def add_button(self, text: str, command=None, **kwargs):
        button = ctk.CTkButton(self, text=text, command=command, **kwargs)
        button.pack(pady=5)
        return button

    def add_checkbox(self, text: str, variable=None, **kwargs):
        checkbox = ctk.CTkCheckBox(self, text=text, variable=variable, **kwargs)
        checkbox.pack(pady=5)
        return checkbox
