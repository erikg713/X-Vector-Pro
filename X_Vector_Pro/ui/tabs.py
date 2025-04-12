ui/tabs.py

import customtkinter as ctk from ui.tabs_brute import load_brute_tab from ui.tabs_recon import load_recon_tab from ui.tabs_scanner import load_scanner_tab from ui.tabs_exploits import load_exploit_tab from ui.tabs_logs import load_logs_tab from ui.tabs_settings import load_settings_tab from ui.tabs_fullauto import load_fullauto_tab from ui.tabs_findings import load_findings_tab

def init_tabs(tabs, app, settings): recon_tab = tabs.add("Recon") scanner_tab = tabs.add("Scanner") brute_tab = tabs.add("Brute Force") exploit_tab = tabs.add("Exploits") logs_tab = tabs.add("Logs") settings_tab = tabs.add("Settings") fullauto_tab = tabs.add("Full Auto") findings_tab = tabs.add("Findings")

load_recon_tab(recon_tab)
load_scanner_tab(scanner_tab)
load_brute_tab(brute_tab)
load_exploit_tab(exploit_tab)
load_logs_tab(logs_tab)
load_settings_tab(settings_tab, settings)
load_fullauto_tab(fullauto_tab)
load_findings_tab(findings_tab)

