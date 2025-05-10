import customtkinter as ctk
import threading
from core.controller import start_brute_force

class BruteTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Brute Force", font=("Segoe UI", 18, "bold")).pack(pady=10)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Target XML-RPC URL")
        self.url_entry.pack(pady=10, padx=20, fill="x")

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=10, padx=20, fill="x")

        self.status_var = ctk.StringVar(value="Idle")
        ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray").pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start Brute Force", command=self.run_brute_threaded)
        self.start_button.pack(pady=10)

    def run_brute_threaded(self):
        url = self.url_entry.get()
        user = self.user_entry.get()

        if not url or not user:
            self.status_var.set("Please enter both URL and username.")
            return

        self.status_var.set("Running brute force...")
        threading.Thread(target=self.run_brute_force, args=(url, user), daemon=True).start()

    def run_brute_force(self, url, user):
        try:
            start_brute_force(url, user)
            self.status_var.set("Brute force completed.")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
