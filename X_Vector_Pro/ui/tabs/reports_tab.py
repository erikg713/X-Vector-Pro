import customtkinter as ctk
import os
import time
from datetime import datetime
from utils.logger import log_to_central
from utils.report_utils import export_to_pdf, export_to_csv, email_report
import tkinter.messagebox as msgbox

class ReportsTab:
    def __init__(self, parent):
        self.parent = parent
        self.reports = self.load_reports()
        
        # Initialize UI components
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI for the Reports Tab"""
        # Title label
        ctk.CTkLabel(self.parent, text="Reports - View and Export", font=("Segoe UI", 14)).pack(pady=(10, 4))

        # Search bar
        ctk.CTkLabel(self.parent, text="Search Reports by Target or Date", font=("Segoe UI", 12)).pack(pady=(10, 4))
        self.search_entry = ctk.CTkEntry(self.parent, width=500)
        self.search_entry.pack(pady=(0, 10))

        # Search button
        self.search_button = ctk.CTkButton(self.parent, text="Search", command=self.search_reports, width=120)
        self.search_button.pack(pady=(5, 10))

        # Display previous reports
        self.report_listbox = ctk.CTkListbox(self.parent, width=800, height=300)
        self.report_listbox.pack(pady=(10, 20))

        # Add a scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.parent, orientation="vertical", command=self.report_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.report_listbox.configure(yscrollcommand=self.scrollbar.set)

        # Export Buttons
        self.export_pdf_button = ctk.CTkButton(self.parent, text="Export as PDF", command=self.export_pdf, width=180)
        self.export_pdf_button.pack(side="left", padx=10, pady=(5, 20))

        self.export_csv_button = ctk.CTkButton(self.parent, text="Export as CSV", command=self.export_csv, width=180)
        self.export_csv_button.pack(side="left", padx=10, pady=(5, 20))

        # Email Report Button
        self.email_button = ctk.CTkButton(self.parent, text="Email Report", command=self.email_report, width=180)
        self.email_button.pack(side="left", padx=10, pady=(5, 20))

        # Populate the report list with existing reports
        self._populate_report_list()

    def _populate_report_list(self):
        """Populate the listbox with available reports"""
        self.report_listbox.delete(0, "end")
        for report in self.reports:
            self.report_listbox.insert("end", f"{report['target']} - {report['date']} - {report['status']}")

    def load_reports(self):
        """Load all reports from the reports directory"""
        report_dir = "reports/"
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        reports = []
        for filename in os.listdir(report_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(report_dir, filename), "r") as file:
                    content = file.read().splitlines()
                    # Parsing the report to get basic info like target, date, and status
                    target = content[1].split(":")[1].strip()
                    date = content[0].split("-")[1].strip()
                    status = "Completed" if "Exploit completed" in content else "Failed"
                    reports.append({"filename": filename, "target": target, "date": date, "status": status})
        return reports

    def search_reports(self):
        """Search the reports list by target or date"""
        query = self.search_entry.get().lower()
        filtered_reports = [r for r in self.reports if query in r['target'].lower() or query in r['date'].lower()]
        
        # Re-populate the listbox with filtered results
        self.report_listbox.delete(0, "end")
        for report in filtered_reports:
            self.report_listbox.insert("end", f"{report['target']} - {report['date']} - {report['status']}")

    def export_pdf(self):
        """Export the selected report as PDF"""
        selected_report = self.get_selected_report()
        if selected_report:
            report_content = self.get_report_content(selected_report)
            export_to_pdf(report_content)
            msgbox.showinfo("Export Successful", "The report has been exported as a PDF.")
        else:
            msgbox.showwarning("No Report Selected", "Please select a report from the list.")

    def export_csv(self):
        """Export the selected report as CSV"""
        selected_report = self.get_selected_report()
        if selected_report:
            report_content = self.get_report_content(selected_report)
            export_to_csv(report_content)
            msgbox.showinfo("Export Successful", "The report has been exported as a CSV.")
        else:
            msgbox.showwarning("No Report Selected", "Please select a report from the list.")

    def email_report(self):
        """Email the selected report to a recipient"""
        selected_report = self.get_selected_report()
        if selected_report:
            report_content = self.get_report_content(selected_report)
            email_report(report_content)
            msgbox.showinfo("Email Sent", "The report has been emailed.")
        else:
            msgbox.showwarning("No Report Selected", "Please select a report from the list.")

    def get_selected_report(self):
        """Get the selected report from the list"""
        selected_index = self.report_listbox.curselection()
        if not selected_index:
            return None
        selected_report = self.reports[selected_index[0]]
        return selected_report

    def get_report_content(self, selected_report):
        """Get the content of the selected report"""
        report_filename = selected_report['filename']
        with open(f"reports/{report_filename}", "r") as file:
            content = file.read()
        return content
