import customtkinter as ctk
from tkinter import filedialog
from engine.dirs import DirectoryScanner
from utils.settings import load_settings
from utils.logger import log_to_central
from utils.helpers import load_wordlist
import threading
import re


def is_valid_url(url):
    """
    Validates the format of a URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL format is valid, False otherwise.
    """
    url_pattern = re.compile(r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+([a-zA-Z]{2,})(/.*)?$')
    return bool(url_pattern.match(url))


def load_directory_tab(tab):
    """
    Configures the Directory Scanner tab in the GUI.

    Args:
        tab (customtkinter.CTkFrame): The container frame for the tab.
    """
    # Load application settings and initialize variables
    settings = load_settings()
    findings = {"directories": []}
    scanner_thread = None

    # Header Section
    ctk.CTkLabel(
        tab,
        text="Directory Scanner",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    # Target URL Entry Field
    target_entry = ctk.CTkEntry(
        tab,
        width=500,
        placeholder_text="Enter target URL (e.g., https://example.com)"
    )
    target_entry.pack(pady=5)

    # Wordlist File Path Field
    wordlist_entry = ctk.CTkEntry(
        tab,
        width=500,
        placeholder_text="Select wordlist file"
    )
    wordlist_entry.pack(pady=5)

    # Browse Button for Wordlist
    def browse_wordlist():
        """
        Opens a file dialog to select a wordlist file and updates the entry field.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            wordlist_entry.delete(0, "end")
            wordlist_entry.insert(0, file_path)

    ctk.CTkButton(
        tab,
        text="Browse Wordlist",
        command=browse_wordlist
    ).pack(pady=3)

    # Result Display Box
    result_box = ctk.CTkTextbox(
        tab,
        width=600,
        height=250,
        corner_radius=10
    )
    result_box.pack(pady=10)

    def append_to_result(msg):
        """
        Appends a message to the result display box.

        Args:
            msg (str): The message to append.
        """
        result_box.insert("end", msg + "\n")
        result_box.see("end")

    # Run Scan Logic
    def run_directory_scan():
        """
        Executes the directory scan based on inputs provided by the user.
        """
        try:
            # Retrieve and validate inputs
            target_url = target_entry.get().strip()
            wordlist_path = wordlist_entry.get().strip()

            if not target_url:
                append_to_result("[!] Target URL is required.")
                return

            if not is_valid_url(target_url):
                append_to_result("[!] Invalid URL format. Please provide a valid URL.")
                return

            wordlist = load_wordlist(wordlist_path) if wordlist_path else None

            # Initialize and start the scanner
            append_to_result("[*] Starting directory scan...")
            scanner = DirectoryScanner(
                base_url=target_url,
                logger=log_to_central,
                wordlist=wordlist,
                config=settings
            )
            scanner.run(findings=findings, update_callback=append_to_result)
            append_to_result("[*] Scan completed successfully.")

        except FileNotFoundError:
            append_to_result("[!] Wordlist file not found. Please check the file path.")
        except Exception as e:
            append_to_result(f"[!] An unexpected error occurred: {str(e)}")

    def start_scan_thread():
        """
        Starts the scan in a separate thread to maintain UI responsiveness.
        """
        nonlocal scanner_thread
        if scanner_thread and scanner_thread.is_alive():
            append_to_result("[!] A scan is already running. Please wait for it to complete.")
            return
        scanner_thread = threading.Thread(target=run_directory_scan)
        scanner_thread.start()

    ctk.CTkButton(
        tab,
        text="Start Scan",
        command=start_scan_thread
    ).pack(pady=5)

    # Export Results Logic
    def export_scan_results():
        """
        Exports the scan results to a user-specified file.
        """
        if not findings["directories"]:
            append_to_result("[!] No findings available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    for directory in findings["directories"]:
                        file.write(f"{directory['path']} [{directory['code']}]\n")
                append_to_result(f"[+] Results successfully exported to {file_path}")
            except Exception as e:
                append_to_result(f"[!] Failed to export results: {str(e)}")

    ctk.CTkButton(
        tab,
        text="Export Results",
        command=export_scan_results
    ).pack(pady=5)
