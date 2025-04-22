import os
import base64
import json
import datetime
from customtkinter import *
from tkinter import filedialog, messagebox, END

LOGS_DIR = "logs"

class LogsTab(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.create_widgets()
        self.load_logs()

    def create_widgets(self):
        # Header
        self.title_label = CTkLabel(self, text="Logs", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=(10, 5))

        # Search bar
        self.search_var = StringVar()
        self.search_entry = CTkEntry(self, textvariable=self.search_var, placeholder_text="Search logs...", width=300)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", lambda e: self.search_logs())

        # Log display box
        self.log_display = CTkTextbox(self, width=800, height=500, wrap="word", font=("Courier", 12))
        self.log_display.pack(pady=10)

        # Control buttons
        btn_frame = CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=5)

        self.refresh_button = CTkButton(btn_frame, text="Refresh", command=self.load_logs, width=120)
        self.refresh_button.grid(row=0, column=0, padx=10)

        self.export_button = CTkButton(btn_frame, text="Export Selected", command=self.export_logs, width=150)
        self.export_button.grid(row=0, column=1, padx=10)

    def decrypt_log(self, log_path):
        try:
            with open(log_path, "rb") as f:
                encoded_data = f.read()
                decrypted_data = base64.b64decode(encoded_data).decode("utf-8")
                return decrypted_data
        except Exception as e:
            return f"[ERROR decrypting {log_path}]: {e}"

    def load_logs(self):
        self.log_display.delete("1.0", END)
        self.logs = []

        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

        log_files = sorted(os.listdir(LOGS_DIR), reverse=True)
        for log_file in log_files:
            if log_file.endswith(".log"):
                full_path = os.path.join(LOGS_DIR, log_file)
                content = self.decrypt_log(full_path)
                timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")
                self.logs.append((log_file, content))
                self.log_display.insert(END, f"[{timestamp}] {log_file}\n{content}\n{'-' * 80}\n")

    def search_logs(self):
        keyword = self.search_var.get().strip().lower()
        self.log_display.delete("1.0", END)
        for name, content in self.logs:
            if keyword in name.lower() or keyword in content.lower():
                self.log_display.insert(END, f"{name}\n{content}\n{'-' * 80}\n")

    def export_logs(self):
        export_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not export_path:
            return

        try:
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(self.log_display.get("1.0", END))
            messagebox.showinfo("Export Complete", f"Logs exported to:\n{export_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {e}")
