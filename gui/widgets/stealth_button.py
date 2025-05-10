# gui/widgets/stealth_button.py
import customtkinter as ctk

class StealthButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, invisible=False, **kwargs):
        super().__init__(master, text=text, command=command, fg_color="gray20",
                         hover_color="gray10", text_color="white", **kwargs)
        if invisible:
            self.configure(fg_color="transparent", text="", hover_color="transparent")
