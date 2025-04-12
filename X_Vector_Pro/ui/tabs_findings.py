ui/tabs_findings.py

import customtkinter as ctk import os, json from tkinter import messagebox

current_project_path = "project"  # You can adjust or load this dynamically findings_list = [] selected_finding_index = None

def load_findings_tab(tab): global findings_listbox, title_entry, cve_entry, severity_menu, url_entry global desc_box, poc_box, rec_box, status_menu

ctk.CTkLabel(tab, text="Saved Findings").pack(pady=5)
findings_listbox = ctk.CTkTextbox(tab, height=150, width=600)
findings_listbox.pack(pady=5)

def load_findings():
    findings_listbox.delete("0.0", "end")
    global findings_list
    findings_list = []

    path = os.path.join(current_project_path, "findings.json")
    if not os.path.exists(path):
        findings_listbox.insert("end", "[!] No findings yet.\n")
        return

    try:
        with open(path, "r") as f:
            findings_list = json.load(f)

        for i, fnd in enumerate(findings_list):
            findings_listbox.insert("end", f"{i+1}. [{fnd['status']}] {fnd['title']} ({fnd['severity']})\n")
    except Exception as e:
        findings_listbox.insert("end", f"[!] Error loading findings: {e}\n")

def delete_last_finding():
    if not findings_list:
        return
    findings_list.pop()
    try:
        with open(os.path.join(current_project_path, "findings.json"), "w") as f:
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
        with open(os.path.join(current_project_path, "findings.json"), "w") as f:
            json.dump(findings_list, f, indent=2)
        load_findings()
    except Exception as e:
        messagebox.showerror("Error", f"Could not update finding: {e}")

ctk.CTkButton(tab, text="Delete Last Finding", command=delete_last_finding).pack(pady=5)
ctk.CTkButton(tab, text="Update Selected Finding", command=update_finding).pack(pady=5)

load_findings()

