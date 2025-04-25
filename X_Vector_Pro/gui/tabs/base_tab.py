import sys

# Check if customtkinter or PyQt5 is available and import accordingly
if "customtkinter" in sys.modules:
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

elif "PyQt5" in sys.modules:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

    class BaseTab(QWidget):
        def __init__(self, parent=None, title: str = ""):
            super().__init__(parent)
            self.title = title
            self.setup_ui()

        def setup_ui(self):
            layout = QVBoxLayout(self)
            if self.title:
                label = QLabel(self.title)
                label.setStyleSheet("font: bold 20px Segoe UI;")
                layout.addWidget(label)

        def add_section_label(self, text: str):
            label = QLabel(text)
            label.setStyleSheet("font: bold 14px Segoe UI; color: white;")
            self.layout().addWidget(label)
            return label

        def add_separator(self):
            separator = QWidget(self)
            separator.setStyleSheet("height: 1px; background-color: #444;")
            self.layout().addWidget(separator)
            return separator
