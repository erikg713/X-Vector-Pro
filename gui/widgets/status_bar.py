# gui/widgets/status_bar.py
import customtkinter as ctk

class StatusBar(ctk.CTkLabel):
    def __init__(self, master, text="Ready"):
        super().__init__(master, text=text, anchor="w", fg_color="gray15", text_color="white")
        self.pack(side="bottom", fill="x")

    def update_status(self, new_text):
        self.configure(text=new_text)
