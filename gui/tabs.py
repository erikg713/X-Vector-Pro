from gui.recon_tab import ReconTab
# from gui.brute_tab import BruteTab
# from gui.exploit_tab import ExploitTab
# from gui.reports_tab import ReportsTab

def init_tabs(parent_frame, app):
    tabs = {}

    # Create tab frames and attach them to the main content frame (but keep hidden initially)
    tabs["Recon"] = ReconTab(parent_frame)
    # tabs["Brute"] = BruteTab(parent_frame)
    # tabs["Exploit"] = ExploitTab(parent_frame)
    # tabs["Reports"] = ReportsTab(parent_frame)

    for tab in tabs.values():
        tab.pack_forget()

    return tabs
