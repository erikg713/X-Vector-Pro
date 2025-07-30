# gui/main.py
import threading
import customtkinter as ctk
from core.controller import XVectorController

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class XVectorProGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro GUI Tool")
        self.geometry("900x700")

        self.controller = None
        self.current_thread = None

        self.tab_view = ctk.CTkTabview(self, width=880, height=650)
        self.tab_view.pack(padx=10, pady=10, fill="both", expand=True)

        # Add tabs
        self.tab_view.add("Auto Mode")
        self.tab_view.add("Plugin Scan")
        self.tab_view.add("Brute Force")
        self.tab_view.add("CVE Checks")

        self.build_auto_mode_tab()
        self.build_plugin_scan_tab()
        self.build_brute_force_tab()
        self.build_cve_check_tab()

        self.tab_view.set("Auto Mode")

    def build_auto_mode_tab(self):
        frame = self.tab_view.tab("Auto Mode")

        ctk.CTkLabel(frame, text="Full Automated Pipeline", font=("Segoe UI", 18)).pack(pady=10)

        self.auto_target_entry = ctk.CTkEntry(frame, placeholder_text="Enter target domain or IP")
        self.auto_target_entry.pack(pady=10, padx=20, fill="x")

        self.auto_start_btn = ctk.CTkButton(frame, text="Run Full Pipeline", command=self.run_full_pipeline)
        self.auto_start_btn.pack(pady=10)

        self.auto_output = ctk.CTkTextbox(frame, height=400)
        self.auto_output.pack(padx=20, pady=10, fill="both", expand=True)
        self.auto_output.configure(state="disabled")

    def run_full_pipeline(self):
        target = self.auto_target_entry.get().strip()
        if not target:
            self.append_text(self.auto_output, "[ERROR] Please enter a valid target.\n")
            return
        if self.current_thread and self.current_thread.is_alive():
            self.append_text(self.auto_output, "[WARN] A scan is already running.\n")
            return

        self.controller = XVectorController(target)
        self.append_text(self.auto_output, f"[INFO] Starting full pipeline against {target}...\n")
        self.current_thread = threading.Thread(target=self._full_pipeline_thread)
        self.current_thread.start()

    def _full_pipeline_thread(self):
        try:
            results = {}
            self.append_text(self.auto_output, "[INFO] Running Recon...\n")
            results['subdomains'] = self.controller.run_recon()
            self.append_text(self.auto_output, f"[RESULT] Found subdomains: {results['subdomains']}\n")

            self.append_text(self.auto_output, "[INFO] Running Plugin Scan...\n")
            results['plugins'] = self.controller.run_plugin_scan()
            self.append_text(self.auto_output, f"[RESULT] Plugins found: {results['plugins']}\n")

            self.append_text(self.auto_output, "[INFO] Running Brute Force...\n")
            self.controller.run_brute_force()
            self.append_text(self.auto_output, "[RESULT] Brute force completed\n")

            self.append_text(self.auto_output, "[INFO] Running CVE Check...\n")
            results['cves'] = self.controller.run_cve_check()
            self.append_text(self.auto_output, f"[RESULT] CVEs found: {results['cves']}\n")

            self.append_text(self.auto_output, "[INFO] Full pipeline completed.\n")
        except Exception as e:
            self.append_text(self.auto_output, f"[ERROR] {str(e)}\n")

    def build_plugin_scan_tab(self):
        frame = self.tab_view.tab("Plugin Scan")

        ctk.CTkLabel(frame, text="Plugin Scanner", font=("Segoe UI", 18)).pack(pady=10)

        self.plugin_target_entry = ctk.CTkEntry(frame, placeholder_text="Enter target domain or IP")
        self.plugin_target_entry.pack(pady=10, padx=20, fill="x")

        self.plugin_start_btn = ctk.CTkButton(frame, text="Scan Plugins", command=self.run_plugin_scan)
        self.plugin_start_btn.pack(pady=10)

        self.plugin_output = ctk.CTkTextbox(frame, height=450)
        self.plugin_output.pack(padx=20, pady=10, fill="both", expand=True)
        self.plugin_output.configure(state="disabled")

    def run_plugin_scan(self):
        target = self.plugin_target_entry.get().strip()
        if not target:
            self.append_text(self.plugin_output, "[ERROR] Please enter a valid target.\n")
            return
        if self.current_thread and self.current_thread.is_alive():
            self.append_text(self.plugin_output, "[WARN] Another scan is running.\n")
            return

        self.controller = XVectorController(target)
        self.append_text(self.plugin_output, f"[INFO] Starting plugin scan on {target}...\n")
        self.current_thread = threading.Thread(target=self._plugin_scan_thread)
        self.current_thread.start()

    def _plugin_scan_thread(self):
        try:
            plugins = self.controller.run_plugin_scan()
            self.append_text(self.plugin_output, f"[RESULT] Plugins found: {plugins}\n")
        except Exception as e:
            self.append_text(self.plugin_output, f"[ERROR] {str(e)}\n")

    def build_brute_force_tab(self):
        frame = self.tab_view.tab("Brute Force")

        ctk.CTkLabel(frame, text="Brute Force Engine", font=("Segoe UI", 18)).pack(pady=10)

        self.brute_target_entry = ctk.CTkEntry(frame, placeholder_text="Enter target domain or IP")
        self.brute_target_entry.pack(pady=10, padx=20, fill="x")

        self.brute_start_btn = ctk.CTkButton(frame, text="Start Brute Force", command=self.run_brute_force)
        self.brute_start_btn.pack(pady=10)

        self.brute_output = ctk.CTkTextbox(frame, height=450)
        self.brute_output.pack(padx=20, pady=10, fill="both", expand=True)
        self.brute_output.configure(state="disabled")

    def run_brute_force(self):
        target = self.brute_target_entry.get().strip()
        if not target:
            self.append_text(self.brute_output, "[ERROR] Please enter a valid target.\n")
            return
        if self.current_thread and self.current_thread.is_alive():
            self.append_text(self.brute_output, "[WARN] Another scan is running.\n")
            return

        self.controller = XVectorController(target)
        self.append_text(self.brute_output, f"[INFO] Starting brute force on {target}...\n")
        self.current_thread = threading.Thread(target=self._brute_force_thread)
        self.current_thread.start()

    def _brute_force_thread(self):
        try:
            self.controller.run_brute_force()
            self.append_text(self.brute_output, "[RESULT] Brute force completed\n")
        except Exception as e:
            self.append_text(self.brute_output, f"[ERROR] {str(e)}\n")

    def build_cve_check_tab(self):
        frame = self.tab_view.tab("CVE Checks")

        ctk.CTkLabel(frame, text="CVE Scanner", font=("Segoe UI", 18)).pack(pady=10)

        self.cve_target_entry = ctk.CTkEntry(frame, placeholder_text="Enter target domain or IP")
        self.cve_target_entry.pack(pady=10, padx=20, fill="x")

        self.cve_start_btn = ctk.CTkButton(frame, text="Run CVE Scan", command=self.run_cve_check)
        self.cve_start_btn.pack(pady=10)

        self.cve_output = ctk.CTkTextbox(frame, height=450)
        self.cve_output.pack(padx=20, pady=10, fill="both", expand=True)
        self.cve_output.configure(state="disabled")

    def run_cve_check(self):
        target = self.cve_target_entry.get().strip()
        if not target:
            self.append_text(self.cve_output, "[ERROR] Please enter a valid target.\n")
            return
        if self.current_thread and self.current_thread.is_alive():
            self.append_text(self.cve_output, "[WARN] Another scan is running.\n")
            return

        self.controller = XVectorController(target)
        self.append_text(self.cve_output, f"[INFO] Starting CVE check on {target}...\n")
        self.current_thread = threading.Thread(target=self._cve_check_thread)
        self.current_thread.start()

    def _cve_check_thread(self):
        try:
            cves = self.controller.run_cve_check()
            self.append_text(self.cve_output, f"[RESULT] CVEs found: {cves}\n")
        except Exception as e:
            self.append_text(self.cve_output, f"[ERROR] {str(e)}\n")

    def append_text(self, text_widget, text):
        text_widget.configure(state="normal")
        text_widget.insert("end", text)
        text_widget.see("end")
        text_widget.configure(state="disabled")


if __name__ == "__main__":
    app = XVectorProGUI()
    app.mainloop()
