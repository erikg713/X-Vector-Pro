# gui/widgets/sidebar_nav.py
import customtkinter as ctk

class SidebarNav(ctk.CTkFrame):
    def __init__(self, master, tabs, callback):
        super().__init__(master, fg_color="gray10", width=150)
        self.pack_propagate(0)
        for tab in tabs:
            btn = ctk.CTkButton(self, text=tab, command=lambda t=tab: callback(t), fg_color="gray20")
            btn.pack(fill="x", pady=2, padx=5)
