import customtkinter as ctk
from tkinter import filedialog
from engine.dirs import DirectoryScanner
from utils.settings import load_settings
from utils.logger import log_to_central
from utils.helpers import load_wordlist
import threading

def is_valid_url(url):
    """Placeholder function to validate a URL."""
    import re
    pattern = re.compile(r'^(https?://)?(www\.)?([a-zA-Z0-9]+)(\.[a-zA-Z]{2,})+')
    return bool(pattern.match(url))

def load_directory_tab(tab):
    """
    Sets up the Directory Scanner tab in the GUI.

    Args:
        tab (customtkinter.CTkFrame): The container frame for the tab.
    """
    settings = load_settings()
    findings = {"directories": []}
    scanner_thread = None

    # Header
    ctk.CTkLabel(tab, text="Directory Scanner", font=("Arial", 20, "bold")).pack(pady=10)

    # Target Entry
    target_entry = ctk.CTkEntry(tab, width=500, placeholder_text="Enter target URL (e.g., https://example.com)")
    target_entry.pack(pady=5)

    # Wordlist Path
    wordlist_entry = ctk.CTkEntry(tab, width=500, placeholder_text="Select wordlist")
    wordlist_entry.pack(pady=5)

    def browse_wordlist():
        """Opens a file dialog to select a wordlist file."""
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            wordlist_entry.delete(0, "end")
            wordlist_entry.insert(0, path)

    ctk.CTkButton(tab, text="Browse Wordlist", command=browse_wordlist).pack(pady=3)

    # Result Display
    result_box = ctk.CTkTextbox(tab, width=600, height=250, corner_radius=10)
    result_box.pack(pady=10)

    def update_output(msg):
        """Updates the result display with a message."""
        result_box.insert("end", msg + "\n")
        result_box.see("end")

    def run_scan():
        """
        Initiates a directory scan based on user input from the GUI elements.
        """
        try:
            # Retrieve and validate inputs
            target_url = target_entry.get().strip()
            wordlist_path = wordlist_entry.get().strip()
            wordlist = load_wordlist(wordlist_path) if wordlist_path else None

            if not target_url:
                update_output("[!] Target URL required.")
                return
            
            if not is_valid_url(target_url):
                update_output("[!] Invalid URL provided.")
                return

            # Initialize and execute scanner
            update_output("[*] Initializing directory scanner...")
            scanner = DirectoryScanner(
                base_url=target_url,
                logger=log_to_central,
                wordlist=wordlist,
                config=settings
            )
            scanner.run(findings=findings, update_callback=update_output)
            update_output("[*] Scan complete.")
        
        except FileNotFoundError as e:
            update_output(f"[!] Wordlist file not found: {e}")
        except Exception as e:
            update_output(f"[!] An error occurred: {e}")

    def start_thread():
        """Starts the scan in a separate thread."""
        nonlocal scanner_thread
        if scanner_thread and scanner_thread.is_alive():
            update_output("[!] Scan already running.")
            return
        scanner_thread = threading.Thread(target=run_scan)
        scanner_thread.start()

    ctk.CTkButton(tab, text="Start Scan", command=start_thread).pack(pady=5)

    # Export Button
    def export_results():
        """Exports the scan results to a file."""
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
