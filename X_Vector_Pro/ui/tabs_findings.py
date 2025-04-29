# ui/tabs_findings.py

import customtkinter as ctk
import os
import json
from tkinter import messagebox

current_project_path = "project"
findings_list = []
selected_finding_index = None

def load_findings_tab(tab):
    global findings_listbox, title_entry, cve_entry, severity_menu, url_entry
    global desc_box, poc_box, rec_box, status_menu

    ctk.CTkLabel(tab, text="Saved Findings", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
    findings_listbox = ctk.CTkTextbox(tab, height=120, width=600)
    findings_listbox.pack(pady=5)

    # Input Form Frame
    form_frame = ctk.CTkFrame(tab)
    form_frame.pack(pady=10)

    # Title
    ctk.CTkLabel(form_frame, text="Title:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    title_entry = ctk.CTkEntry(form_frame, width=300)
    title_entry.grid(row=0, column=1, padx=5, pady=3)

    # CVE
    ctk.CTkLabel(form_frame, text="CVE:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    cve_entry = ctk.CTkEntry(form_frame, width=300)
    cve_entry.grid(row=1, column=1, padx=5, pady=3)

    # Severity
    ctk.CTkLabel(form_frame, text="Severity:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    severity_menu = ctk.CTkOptionMenu(form_frame, values=["Low", "Medium", "High", "Critical"])
    severity_menu.grid(row=2, column=1, padx=5, pady=3)

    # URL
    ctk.CTkLabel(form_frame, text="URL:").grid(row=3, column=0, sticky="e", padx=5, pady=3)
    url_entry = ctk.CTkEntry(form_frame, width=300)
    url_entry.grid(row=3, column=1, padx=5, pady=3)

    # Description
    ctk.CTkLabel(form_frame, text="Description:").grid(row=4, column=0, sticky="ne", padx=5, pady=3)
    desc_box = ctk.CTkTextbox(form_frame, height=60, width=300)
    desc_box.grid(row=4, column=1, padx=5, pady=3)

    # PoC
    ctk.CTkLabel(form_frame, text="Proof of Concept:").grid(row=5, column=0, sticky="ne", padx=5, pady=3)
    poc_box = ctk.CTkTextbox(form_frame, height=60, width=300)
    poc_box.grid(row=5, column=1, padx=5, pady=3)

    # Recommendation
    ctk.CTkLabel(form_frame, text="Recommendation:").grid(row=6, column=0, sticky="ne", padx=5, pady=3)
    rec_box = ctk.CTkTextbox(form_frame, height=60, width=300)
    rec_box.grid(row=6, column=1, padx=5, pady=3)

    # Status
    ctk.CTkLabel(form_frame, text="Status:").grid(row=7, column=0, sticky="e", padx=5, pady=3)
    status_menu = ctk.CTkOptionMenu(form_frame, values=["Open", "In Progress", "Resolved", "Closed"])
    status_menu.grid(row=7, column=1, padx=5, pady=3)

    # Buttons
    ctk.CTkButton(tab, text="Delete Last Finding", command=delete_last_finding).pack(pady=5)
    ctk.CTkButton(tab, text="Update Selected Finding", command=update_finding).pack(pady=5)

    load_findings()

def load_findings():
    findings_listbox.delete("0.0", "end")
    global findings_list
    findings_list = []

    path = os.path.join(current_project_path, "findings.json")
    if not os.path.exists(path):
        findings_listbox.insert("end", "[!] No findings yet.\n")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            findings_list = json.load(f)

        for i, fnd in enumerate(findings_list):
            findings_listbox.insert("end", f"{i+1}. [{fnd['status']}] {fnd['title']} ({fnd['severity']})\n")
    except Exception as e:
        findings_listbox.insert("end", f"[!] Error loading findings: {e}\n")

def delete_last_finding():
    if not findings_list:
        messagebox.showinfo("Info", "No findings to delete.")
        return

    findings_list.pop()
    try:
        with open(os.path.join(current_project_path, "findings.json"), "w", encoding="utf-8") as f:
            json.dump(findings_list, f, indent=2)
        load_findings()
    except Exception as e:
        messagebox.showerror("Error", f"Delete failed: {e}")

def update_finding():
    global selected_finding_index
    if selected_finding_index is None:
        messagebox.showerror("Error", "No finding selected to update.")
        return

    updated = {
        "title": title_entry.get().strip(),
        "cve": cve_entry.get().strip(),
        "severity": severity_menu.get(),
        "url": url_entry.get().strip(),
        "description": desc_box.get("1.0", "end").strip(),
        "poc": poc_box.get("1.0", "end").strip(),
        "recommendation": rec_box.get("1.0", "end").strip(),
        "status": status_menu.get()
    }

    findings_list[selected_finding_index] = updated
    try:
        with open(os.path.join(current_project_path, "findings.json"), "w", encoding="utf-8") as f:
            json.dump(findings_list, f, indent=2)
        load_findings()
    except Exception as e:
        messagebox.showerror("Error", f"Could not update finding: {e}")
