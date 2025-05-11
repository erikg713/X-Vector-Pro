import customtkinter as ctk
from gui.auto_tab import build_tab as build_auto_tab
from gui.exploits_tab import build_tab as build_exploits_tab
from gui.recon_tab import build_tab as build_recon_tab
from gui.scanner_tab import build_tab as build_scanner_tab
from gui.reports_tab import build_tab as build_reports_tab
from gui.stealth_tab import build_tab as build_stealth_tab

# App setup
app = ctk.CTk()
app.title("X-Vector Pro")
app.geometry("1000x700")

tabs = ctk.CTkTabview(app)
tabs.pack(expand=True, fill="both", padx=10, pady=10)

# Create each tab
tab_auto = tabs.add("Auto Mode")
tab_auto_content = build_auto_tab(tab_auto)
tab_auto_content.pack(fill="both", expand=True)

tab_exploits = tabs.add("Exploits")
tab_exploits_content = build_exploits_tab(tab_exploits)
tab_exploits_content.pack(fill="both", expand=True)

tab_recon = tabs.add("Recon")
tab_recon_content = build_recon_tab(tab_recon)
tab_recon_content.pack(fill="both", expand=True)

tab_scanner = tabs.add("Scanner")
tab_scanner_content = build_scanner_tab(tab_scanner)
tab_scanner_content.pack(fill="both", expand=True)

tab_reports = tabs.add("Reports")
tab_reports_content = build_reports_tab(tab_reports)
tab_reports_content.pack(fill="both", expand=True)

tab_stealth = tabs.add("Stealth")
tab_stealth_content = build_stealth_tab(tab_stealth)
tab_stealth_content.pack(fill="both", expand=True)

app.mainloop()
