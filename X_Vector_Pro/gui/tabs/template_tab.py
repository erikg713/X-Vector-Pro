# gui/tabs/template_tab.py

import customtkinter as ctk

class TemplateTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Template Tab",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(
            self,
            text="This is your starting point for any tab.",
            font=("Arial", 16),
            text_color="#cfcfcf"
        )
        subtitle.pack(pady=10)

        action_button = ctk.CTkButton(
            self,
            text="Run Action",
            command=self.dummy_action,
            fg_color="#2b2b2b",
            hover_color="#3c3c3c"
        )
        action_button.pack(pady=20)

    def dummy_action(self):
        print("Action triggered!")
