# gui/tabs/base_tab.py

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

from PyQt5.QtWidgets import QWidget

class BaseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        raise NotImplementedError("Must be implemented in subclass")
