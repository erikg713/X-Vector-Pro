import customtkinter as ctk
import os

class TrainingTab(ctk.CTkFrame):
    def __init__(self, master, log_path="/mnt/data/xvector_log.txt", **kwargs):
        super().__init__(master, **kwargs)
        self.log_path = log_path

        self.title = ctk.CTkLabel(self, text="X-Vector Training Logs", font=ctk.CTkFont(size=18, weight="bold"))
        self.title.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=700, height=400, wrap="word")
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Logs", command=self.load_logs)
        self.refresh_button.pack(pady=5)

        self.load_logs()

    def load_logs(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as file:
                log_text = file.read()
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", log_text)
        else:
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", "Log file not found.")
