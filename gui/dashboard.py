import customtkinter as ctk
from core.controller import start_brute_force
import threading

def launch_gui():
    app = ctk.CTk()
    app.geometry("600x400")
    app.title("X-Vector Pro")

    label = ctk.CTkLabel(app, text="X-Vector Pro", font=("Helvetica", 22))
    label.pack(pady=20)

    url_entry = ctk.CTkEntry(app, placeholder_text="Target XML-RPC URL")
    url_entry.pack(pady=10)

    user_entry = ctk.CTkEntry(app, placeholder_text="Username")
    user_entry.pack(pady=10)

    def run_brute():
        url = url_entry.get()
        user = user_entry.get()
        threading.Thread(target=start_brute_force, args=(url, user)).start()

    start_button = ctk.CTkButton(app, text="Start Brute Force", command=run_brute)
    start_button.pack(pady=20)

    app.mainloop()
