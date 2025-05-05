import tkinter as tk
from tkinter import ttk, filedialog
from engine.brute_engine import BruteForcer
import threading

class BruteTab:
    def __init__(self, parent, toast_manager):
        self.toast = toast_manager
        self.frame = ttk.Frame(parent)

        self.target_var = tk.StringVar()
        self.wordlist_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Idle")
        self.running = False

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self.frame, text="Brute Force Module", font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))

        # Target Input
        target_frame = ttk.Frame(self.frame)
        target_frame.pack(pady=(5, 0))
        ttk.Label(target_frame, text="Target URL:").pack(side="left", padx=5)
        ttk.Entry(target_frame, textvariable=self.target_var, width=40).pack(side="left")

        # Wordlist Selection
        wordlist_frame = ttk.Frame(self.frame)
        wordlist_frame.pack(pady=5)
        ttk.Label(wordlist_frame, text="Wordlist:").pack(side="left", padx=5)
        ttk.Entry(wordlist_frame, textvariable=self.wordlist_var, width=30).pack(side="left")
        ttk.Button(wordlist_frame, text="Browse", command=self._browse_wordlist).pack(side="left", padx=5)

        # Start Button
        self.run_btn = ttk.Button(self.frame, text="Run Brute Force", command=self._start_brute_force)
        self.run_btn.pack(pady=10)

        # Status
        self.status_label = ttk.Label(self.frame, textvariable=self.status_var, foreground="#CCCCCC")
        self.status_label.pack(pady=(5, 10))

    def _browse_wordlist(self):
        path = filedialog.askopenfilename(title="Select Wordlist File", filetypes=[("Text Files", "*.txt")])
        if path:
            self.wordlist_var.set(path)

    def _start_brute_force(self):
        if self.running:
            self.toast.show("Brute force already running.")
            return

        target = self.target_var.get().strip()
        wordlist = self.wordlist_var.get().strip()

        if not target or not wordlist:
            self.toast.show("Please provide both target and wordlist.")
            return

        self.status_var.set("Brute forcing in progress...")
        self.run_btn.config(state="disabled")
        self.running = True

        thread = threading.Thread(target=self._run_brute, args=(target, wordlist))
        thread.start()

    def _run_brute(self, target, wordlist):
        try:
            brute = BruteForcer(target, wordlist, logger=self._log, stealth=True)
            brute.run()
            self.status_var.set("Brute force complete.")
            self.toast.show("Brute force completed.")
        except Exception as e:
            self.status_var.set("Error during brute force.")
            self.toast.show(f"Brute force error: {str(e)}")
        finally:
            self.run_btn.config(state="normal")
            self.running = False

    def _log(self, msg):
        print(f"[BRUTE] {msg}")
