# gui/widgets/toast_notifier.py
import customtkinter as ctk

class ToastNotifier(ctk.CTkToplevel):
    def __init__(self, master, message, duration=2000):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry("250x50+100+100")
        self.label = ctk.CTkLabel(self, text=message, text_color="white")
        self.label.pack(expand=True, fill="both")
        self.after(duration, self.destroy)
