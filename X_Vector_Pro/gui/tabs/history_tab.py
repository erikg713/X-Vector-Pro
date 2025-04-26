import os
import json
import threading
import time
import shutil
from tkinter import filedialog
import customtkinter as ctk

LOG_DIR = "logs"

class HistoryTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.loading = False
        self.spinner_index = 0
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.build_ui()

    def build_ui(self):
        # Title
        title_frame = ctk.CTkFrame(self)
        title_frame.pack(pady=(10, 5))
        self.title_label = ctk.CTkLabel(title_frame, text="Log History Viewer", font=("Segoe UI", 20, "bold"))
        self.title_label.pack(side="left")

        self.spinner_label = ctk.CTkLabel(title_frame, text="", font=("Consolas", 20))
        self.spinner_label.pack(side="left", padx=(10,0))

        # Dropdown + Buttons Row
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=(5, 5))

        self.dropdown = ctk.CTkOptionMenu(top_frame, values=["No logs available"], command=self.load_selected_log)
        self.dropdown.pack(side="left", padx=(0, 10))

        self.refresh_button = ctk.CTkButton(top_frame, text="Refresh Logs", command=self.refresh_log_list)
        self.refresh_button.pack(side="left", padx=(0, 10))

        self.latest_button = ctk.CTkButton(top_frame, text="View Latest", command=self.view_latest_log)
        self.latest_button.pack(side="left", padx=(0, 10))

        self.download_button = ctk.CTkButton(top_frame, text="Download Log", command=self.download_selected_log)
        self.download_button.pack(side="left", padx=(0, 10))

        self.delete_button = ctk.CTkButton(top_frame, text="Delete Log", command=self.delete_selected_log)
        self.delete_button.pack(side="left", padx=(0, 10))

        self.clear_all_button = ctk.CTkButton(top_frame, text="Clear All", fg_color="red", command=self.clear_all_logs)
        self.clear_all_button.pack(side="left")

        # Viewer
        self.viewer = ctk.CTkTextbox(self, wrap="word", height=400)
        self.viewer.pack(padx=20, pady=10, fill="both", expand=True)
        self.viewer.insert("end", "Log contents will appear here...\n")
        self.viewer.configure(state="disabled")

        # Toast Label
        self.toast = ctk.CTkLabel(self, text="", font=("Segoe UI", 12))
        self.toast.pack(pady=(0, 10))

        # Threads
        threading.Thread(target=self.auto_refresh_loop, daemon=True).start()
        threading.Thread(target=self.spinner_animation_loop, daemon=True).start()

        self.refresh_log_list()

    def refresh_log_list(self, keep_current=False):
        self.loading = True
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        files = sorted((f for f in os.listdir(LOG_DIR) if f.endswith(".json")), reverse=True)
        current_selection = self.dropdown.get()

        if files:
            self.dropdown.configure(values=files)
            if not keep_current or current_selection not in files:
                self.dropdown.set(files[0])
                self.load_selected_log(files[0])
        else:
            self.dropdown.configure(values=["No logs available"])
            self.dropdown.set("No logs available")
            self.clear_viewer()

        self.loading = False

    def load_selected_log(self, filename):
        if filename == "No logs available":
            self.clear_viewer()
            return

        full_path = os.path.join(LOG_DIR, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Pretty format JSON
            try:
                parsed = json.loads(content)
                content = json.dumps(parsed, indent=4)
            except json.JSONDecodeError:
                pass  # Not valid JSON, just show raw

            self.viewer.configure(state="normal")
            self.viewer.delete("1.0", "end")
            self.viewer.insert("end", content)
            self.viewer.configure(state="disabled")
            self.show_toast(f"Loaded {filename}", "green")
        except Exception as e:
            self.viewer.configure(state="normal")
            self.viewer.delete("1.0", "end")
            self.viewer.insert("end", f"Error reading log: {str(e)}")
            self.viewer.configure(state="disabled")
            self.show_toast("Error loading log.", "red")

    def clear_viewer(self):
        self.viewer.configure(state="normal")
        self.viewer.delete("1.0", "end")
        self.viewer.insert("end", "No log selected.\n")
        self.viewer.configure(state="disabled")

    def delete_selected_log(self):
        filename = self.dropdown.get()
        if filename == "No logs available":
            return

        full_path = os.path.join(LOG_DIR, filename)
        if os.path.exists(full_path):
            os.remove(full_path)
            self.show_toast(f"Deleted {filename}", "red")
            self.refresh_log_list()
        else:
            self.show_toast("File not found.", "red")

    def download_selected_log(self):
        filename = self.dropdown.get()
        if filename == "No logs available":
            return

        src_path = os.path.join(LOG_DIR, filename)
        dest_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=filename)
        if dest_path:
            shutil.copy(src_path, dest_path)
            self.show_toast("Log downloaded!", "green")

    def clear_all_logs(self):
        confirm = ctk.CTkInputDialog(text="Type 'CLEAR' to delete all logs:", title="Confirm Clear All")
        result = confirm.get_input()
        if result == "CLEAR":
            for file in os.listdir(LOG_DIR):
                if file.endswith(".json"):
                    os.remove(os.path.join(LOG_DIR, file))
            self.show_toast("All logs cleared!", "red")
            self.refresh_log_list()
        else:
            self.show_toast("Clear operation cancelled.", "yellow")

    def view_latest_log(self):
        files = sorted((f for f in os.listdir(LOG_DIR) if f.endswith(".json")), reverse=True)
        if files:
            self.dropdown.set(files[0])
            self.load_selected_log(files[0])
        else:
            self.show_toast("No logs found.", "yellow")

    def show_toast(self, message, color="green"):
        self.toast.configure(text=message, text_color=color)
        self.toast.after(3000, lambda: self.toast.configure(text=""))

    def auto_refresh_loop(self):
        while True:
            time.sleep(5)
            self.refresh_log_list(keep_current=True)

    def spinner_animation_loop(self):
        while True:
            if self.loading:
                frame = self.spinner_frames[self.spinner_index]
                self.spinner_label.configure(text=frame)
                self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
            else:
                self.spinner_label.configure(text="")
            time.sleep(0.1)
