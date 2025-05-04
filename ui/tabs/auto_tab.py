import tkinter as tk
from tkinter import ttk
from engine.auto_mode import AutoModeEngine

class AutoTab:
    def __init__(self, parent, toast_manager):
        self.toast = toast_manager
        self.frame = ttk.Frame(parent)

        self.target_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Idle")
        self.running = False

        self._build_ui()

    def _build_ui(self):
        header = ttk.Label(self.frame, text="Auto Mode - Full Recon Chain", font=("Segoe UI", 14, "bold"))
        header.pack(pady=(10, 5))

        entry_frame = ttk.Frame(self.frame)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame, text="Target URL / IP:").pack(side="left", padx=(0, 5))
        entry = ttk.Entry(entry_frame, textvariable=self.target_var, width=40)
        entry.pack(side="left")

        self.run_btn = ttk.Button(self.frame, text="Start Auto Recon", command=self._start_chain)
        self.run_btn.pack(pady=10)

        self.status_label = ttk.Label(self.frame, textvariable=self.status_var, foreground="#CCCCCC")
        self.status_label.pack(pady=(5, 10))

    def _start_chain(self):
        if self.running:
            self.toast.show("Scan already running.")
            return

        target = self.target_var.get().strip()
        if not target:
            self.toast.show("Please enter a valid target.")
            return

        self.status_var.set("Running full auto chain...")
        self.run_btn.config(state="disabled")
        self.running = True

        self.frame.after(100, lambda: self._run_full_mode(target))

    def _run_full_mode(self, target):
        try:
            engine = AutoModeEngine(target, log=self._log, toast=self.toast.show)
            engine.execute_chain()
            self.status_var.set("Auto mode complete.")
            self.toast.show("Auto mode completed successfully.")
        except Exception as e:
            self.status_var.set("Error during auto execution.")
            self.toast.show(f"Auto mode failed: {str(e)}")
        finally:
            self.run_btn.config(state="normal")
            self.running = False

    def _log(self, msg):
        print(f"[AUTO] {msg}")
