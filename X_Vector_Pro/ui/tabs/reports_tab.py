import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from datetime import datetime

REPORTS_DIR = "reports"

class ReportsTab:
    def __init__(self, parent, toast_manager):
        self.toast = toast_manager
        self.frame = ttk.Frame(parent)

        self.reports = []
        self.selected_report = tk.StringVar()
        self.report_content = tk.StringVar()

        self._build_ui()
        self._load_reports()

    def _build_ui(self):
        ttk.Label(self.frame, text="Reports Viewer", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Dropdown to select report
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack(pady=5)
        ttk.Label(dropdown_frame, text="Available Reports:").pack(side="left", padx=5)

        self.dropdown = ttk.OptionMenu(dropdown_frame, self.selected_report, "", command=self._display_report)
        self.dropdown.pack(side="left", padx=5)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Open Report Folder", command=self._open_folder).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Export Report", command=self._export_report).pack(side="left", padx=5)

        # Text view
        self.text_box = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=90, height=25)
        self.text_box.pack(pady=10)

    def _load_reports(self):
        if not os.path.exists(REPORTS_DIR):
            os.makedirs(REPORTS_DIR)

        self.reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".txt")]
        if self.reports:
            self.selected_report.set(self.reports[0])
            self._update_dropdown()
            self._display_report(self.reports[0])
        else:
            self.selected_report.set("No reports found")
            self._update_dropdown()

    def _update_dropdown(self):
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for report in self.reports:
            menu.add_command(label=report, command=lambda r=report: self._display_report(r))

    def _display_report(self, filename):
        try:
            with open(os.path.join(REPORTS_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, content)
        except Exception as e:
            self.toast.show(f"Error reading report: {e}")

    def _export_report(self):
        filename = self.selected_report.get()
        if filename not in self.reports:
            self.toast.show("No valid report selected.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Report As",
            defaultextension=".txt",
            initialfile=filename,
            filetypes=[("Text Files", "*.txt")]
        )
        if save_path:
            try:
                with open(os.path.join(REPORTS_DIR, filename), "r", encoding="utf-8") as src:
                    content = src.read()
                with open(save_path, "w", encoding="utf-8") as dst:
                    dst.write(content)
                self.toast.show("Report exported successfully.")
            except Exception as e:
                self.toast.show(f"Export failed: {e}")

    def _open_folder(self):
        try:
            os.startfile(os.path.abspath(REPORTS_DIR))
        except Exception as e:
            self.toast.show(f"Cannot open folder: {e}")
