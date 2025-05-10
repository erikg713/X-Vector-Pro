# gui/brute_tab.py
import customtkinter as ctk
from tkinter import filedialog
import threading
from core.brute.brute_engine import run_brute_force

def load_brute_tab(parent, app):
    ctk.CTkLabel(parent, text="Target XML-RPC URL (https://example.com/xmlrpc.php)").pack(pady=5)
    target_entry = ctk.CTkEntry(parent, width=700)
    target_entry.pack()

    ctk.CTkLabel(parent, text="Usernames (one per line)").pack(pady=5)
    usernames_box = ctk.CTkTextbox(parent, height=100, width=700)
    usernames_box.pack()

    ctk.CTkLabel(parent, text="Password Wordlist").pack(pady=5)
    wordlist_frame = ctk.CTkFrame(parent)
    wordlist_frame.pack()
    wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
    wordlist_entry.pack(side="left", padx=5)
    browse_btn = ctk.CTkButton(wordlist_frame, text="Browse", command=lambda: browse_file(wordlist_entry))
    browse_btn.pack(side="left")

    output_box = ctk.CTkTextbox(parent, height=200, width=700)
    output_box.pack(pady=10)

    def start_brute():
        threading.Thread(target=run_brute_force, args=(
            target_entry.get().strip(),
            usernames_box.get("1.0", "end").strip().splitlines(),
            wordlist_entry.get().strip(),
            output_box
        )).start()

    ctk.CTkButton(parent, text="Start Brute Force", fg_color="green", command=start_brute).pack(pady=10)

def browse_file(entry):
    path = filedialog.askopenfilename()
    if path:
        entry.delete(0, "end")
        entry.insert(0, path)
