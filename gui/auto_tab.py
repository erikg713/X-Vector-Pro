import customtkinter as ctk
import threading
import re

class AutoTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.target_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Idle")
        self._thread = None

        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Auto Mode: Full Recon, Scan, Brute Force", font=("Arial", 18, "bold")).pack(pady=15)

        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(entry_frame, text="Target URL or IP:").pack(side="left", padx=(0, 10))
        self.target_entry = ctk.CTkEntry(entry_frame, textvariable=self.target_var)
        self.target_entry.pack(side="left", fill="x", expand=True)

        self.start_btn = ctk.CTkButton(entry_frame, text="Start", command=self._on_start)
        self.start_btn.pack(side="left", padx=(10, 0))

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, text_color="gray")
        self.status_label.pack(pady=(0, 10))

        self.output_box = ctk.CTkTextbox(self, height=300, wrap="word")
        self.output_box.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.output_box.configure(state="disabled")

        clear_btn = ctk.CTkButton(self, text="Clear Output", command=self._clear_output)
        clear_btn.pack(pady=(0, 10))

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=20, pady=(0, 10))
        self.progress.stop()
        self.progress.pack_forget()

    def _on_start(self):
        target = self.target_var.get().strip()
        if not self._is_valid_target(target):
            self._append_output("[ERROR] Please enter a valid target URL or IP.\n")
            return

        if self._thread and self._thread.is_alive():
            self._append_output("[WARN] Task already running. Please wait.\n")
            return

        self._set_ui_running(True)
        self._thread = threading.Thread(target=self._run_auto_mode, args=(target,), daemon=True)
        self._thread.start()

    def _run_auto_mode(self, target):
        self._append_output(f"[INFO] Starting full pipeline on target: {target}\n")
        self.status_var.set("Running...")

        self.progress.pack(fill="x", padx=20, pady=(0, 10))
        self.progress.start()

        try:
            # Placeholder for real work
            import time
            for i in range(5):
                self._append_output(f"[INFO] Step {i+1}/5 running...\n")
                time.sleep(1)
            self._append_output("[INFO] Pipeline completed successfully.\n")
        except Exception as e:
            self._append_output(f"[ERROR] {str(e)}\n")
        finally:
            self.status_var.set("Idle")
            self._set_ui_running(False)
            self.progress.stop()
            self.progress.pack_forget()

    def _append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def _clear_output(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def _set_ui_running(self, running):
        self.start_btn.configure(state="disabled" if running else "normal")
        self.target_entry.configure(state="disabled" if running else "normal")

    def _is_valid_target(self, target):
        # Simple validation: match IP or domain-like pattern
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.[A-Za-z]{2,})+$"
        return re.match(ip_pattern, target) or re.match(domain_pattern, target)
