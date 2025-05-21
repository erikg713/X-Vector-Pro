import customtkinter as ctk
from pathlib import Path

class TrainingTab(ctk.CTkFrame):
    """
    TrainingTab provides a UI frame to display and refresh X-Vector training logs.
    """
    def __init__(self, master, log_path="/mnt/data/xvector_log.txt", **kwargs):
        super().__init__(master, **kwargs)
        self.log_path = Path(log_path)

        self._build_widgets()
        self.load_logs()

    def _build_widgets(self):
        # Title
        self.title = ctk.CTkLabel(
            self,
            text="X-Vector Training Logs",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title.pack(pady=(12, 8))

        # Textbox for logs
        self.textbox = ctk.CTkTextbox(
            self,
            width=700,
            height=400,
            wrap="word",
            state="normal"  # Ensure it's editable for inserting/deleting text
        )
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)

        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self,
            text="Refresh Logs",
            command=self.load_logs
        )
        self.refresh_button.pack(pady=(0, 8))

    def load_logs(self):
        """
        Loads the log file content into the textbox.
        If the file doesn't exist or can't be read, displays an error message.
        """
        self.textbox.configure(state="normal")
        try:
            if self.log_path.exists() and self.log_path.is_file():
                log_text = self.log_path.read_text(encoding="utf-8")
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", log_text)
            else:
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", "Log file not found.")
        except Exception as e:
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", f"Error loading logs:\n{e}")
        finally:
            self.textbox.configure(state="disabled")  # Prevent user editing
