# gui/widgets/dark_mode_toggle.py
import customtkinter as ctk

class DarkModeToggle(ctk.CTkSwitch):
    def __init__(self, master, command=None):
        super().__init__(master, text="Dark Mode", command=self.toggle_theme)
        self.command = command
        self.select()  # Default to dark

    def toggle_theme(self):
        theme = "dark" if self.get() else "light"
        ctk.set_appearance_mode(theme)
        if self.command:
            self.command(theme)
