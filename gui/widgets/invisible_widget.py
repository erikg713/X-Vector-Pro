# gui/widgets/invisible_widget.py
import customtkinter as ctk

class InvisibleWidget(ctk.CTkLabel):
    def __init__(self, master, command=None):
        super().__init__(master, text="", width=1, height=1)
        self.bind("<Enter>", lambda e: command() if command else None)
        self.place_forget()  # Hidden by default
