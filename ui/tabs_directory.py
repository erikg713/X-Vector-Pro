import customtkinter as ctk
from tkinter import filedialog
from engine.dirs import DirectoryScanner
from utils.settings import load_settings
from utils.logger import log_to_central
from utils.helpers import load_wordlist
import threading

def load_directory_tab(tab):
    settings = load_settings()
    findings = {"directories": []}
    scanner_thread = None

    # Header
    ctk.CTkLabel(tab, text="Directory Scanner", font=("Arial", 20)).pack(pady=10)

    # Target Entry
    target_entry = ctk.CTkEntry(tab, width=500, placeholder_text="Enter target URL (e.g., https://example.com)")
    target_entry.pack(pady=5)

    # Wordlist Path
    wordlist_entry = ctk.CTkEntry(tab, width=500, placeholder_text="Select wordlist")
    wordlist_entry.pack(pady=5)

    def browse_wordlist():
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            wordlist_entry.delete(0, "end")
            wordlist_entry.insert(0, path)

    ctk.CTkButton(tab, text="Browse Wordlist", command=browse_wordlist).pack(pady=3)

    # Result Display
    result_box = ctk.CTkTextbox(tab, width=600, height=250, corner_radius=10)
    result_box.pack(pady=10)

    def update_output(msg):
        result_box.insert("end", msg + "\n")
        result_box.see("end")

    def run_scan():
        url = target_entry.get().strip()
        wordlist_path = wordlist_entry.get().strip()
        wordlist = load_wordlist(wordlist_path) if wordlist_path else None
        if not url:
            update_output("[!] Target URL required.")
            return

        scanner = DirectoryScanner(base_url=url, logger=log_to_central, wordlist=wordlist, config=settings)
        scanner.run(findings=findings, update_callback=update_output)
        update_output("[*] Scan complete.")

    def start_thread():
        nonlocal scanner_thread
        if scanner_thread and scanner_thread.is_alive():
            update_output("[!] Scan already running.")
            return
        scanner_thread = threading.Thread(target=run_scan)
        scanner_thread.start()

    ctk.CTkButton(tab, text="Start Scan", command=start_thread).pack(pady=5)

    # Export Button
    def export_results():
        if not findings["directories"]:
            update_output("[!] No findings to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, "w") as f:
                for d in findings["directories"]:
                    f.write(f"{d['path']} [{d['code']}]\n")
            update_output(f"[+] Results exported to {path}")

    ctk.CTkButton(tab, text="Export Results", command=export_results).pack(pady=5)
