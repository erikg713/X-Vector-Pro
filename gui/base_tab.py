import threading
import re
import customtkinter as ctk
from core.auto_chain import run_auto_chain  # Your main scanning pipeline function

class AutoTab(BaseTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="Auto Mode: Full Recon, Scan, Exploit", **kwargs)
        self._current_thread = None
        self._build_ui()

    def _build_ui(self):
        self.target_entry = self.add_entry("Enter target IP or domain...")
        self.start_button = self.add_button("Start Full Pipeline", command=self._start_pipeline)
        self.status_label = ctk.CTkLabel(self, text="Idle", text_color="gray")
        self.status_label.pack(pady=(5, 10))

        self.output_box = ctk.CTkTextbox(self, height=300, wrap="word")
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.output_box.configure(state="disabled")

        self.clear_button = self.add_button("Clear Output", command=self.clear_output)

    def _start_pipeline(self):
        target = self.target_entry.get().strip()
        if not self._validate_target(target):
            self._set_status("Invalid target. Enter a valid IP or domain.", "red")
            return

        if self._current_thread and self._current_thread.is_alive():
            self._set_status("Pipeline already running.", "orange")
            return

        self._set_status("Starting pipeline...", "blue")
        self.start_button.configure(state="disabled")
        self._current_thread = threading.Thread(target=self._run_pipeline, args=(target,), daemon=True)
        self._current_thread.start()

    def _run_pipeline(self, target):
        try:
            def gui_callback(text):
                self.append_output(text + "\n")

            results = run_auto_chain(target, gui_callback=gui_callback)
            self.append_output("[INFO] Pipeline completed successfully.\n")
            self._set_status("Idle", "gray")
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
            self._set_status("Error occurred.", "red")
        finally:
            self.start_button.configure(state="normal")

    def _validate_target(self, target):
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        domain_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,}$"
        return re.match(ip_pattern, target) or re.match(domain_pattern, target)

    def append_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def clear_output(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def _set_status(self, message, color="gray"):
        self.status_label.configure(text=message, text_color=color)

