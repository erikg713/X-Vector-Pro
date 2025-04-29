import customtkinter as ctk
import threading, socket, json, re, os, requests, tldextract
import importlib.util, time, datetime

from utils.logger import log_to_central
from engine.recon import ReconScanner
from engine.ports import PortScanner
from engine.dirs import DirectoryScanner
from engine.plugins import PluginScanner
from engine.exploits import ExploitRunner
from engine.report import ReportGenerator

PROFILE_PATH = "auto_profile.json"
FINDINGS_PATH = "fullauto_findings.json"
HTML_REPORT = "fullauto_report.html"

def load_fullauto_tab(tab):
    def run_full_auto_mode():
        url = fullauto_url_entry.get().strip()
        if not url.startswith("http"):
            fullauto_log("[!] Invalid URL. Use full http/https format.")
            return

        fullauto_log("[*] Starting full auto mode...")
        findings = {
            "target": url,
            "started": datetime.datetime.now().isoformat(),
            "title": "",
            "open_ports": [],
            "directories": [],
            "cves": [],
            "exploits": []
        }

        # Recon
        if recon_toggle.get():
            try:
                fullauto_log("[*] Running Recon...")
                ReconScanner(url, fullauto_log).run(findings)
            except Exception as e:
                fullauto_log(f"[!] Recon failed: {e}")

        # Port Scan
        if port_toggle.get():
            try:
                fullauto_log("[*] Running Port Scan...")
                PortScanner(url, fullauto_log).run(findings)
            except Exception as e:
                fullauto_log(f"[!] Port scan failed: {e}")

        # Directory Scan
        if dir_toggle.get():
            try:
                fullauto_log("[*] Running Dir Scan...")
                DirectoryScanner(url, fullauto_log).run(findings)
            except Exception as e:
                fullauto_log(f"[!] Dir scan failed: {e}")

        # Plugin Detection + CVE Match
        found_plugins = []
        if plugin_toggle.get():
            try:
                fullauto_log("[*] Checking for plugins/themes...")
                scanner = PluginScanner(url, fullauto_log)
                found_plugins = scanner.run(findings)
            except Exception as e:
                fullauto_log(f"[!] Plugin check failed: {e}")

        # Exploits
        if exploit_toggle.get():
            try:
                runner = ExploitRunner(url, fullauto_log)
                runner.run(found_plugins, findings)
            except Exception as e:
                fullauto_log(f"[!] Exploit runner error: {e}")

        findings["finished"] = datetime.datetime.now().isoformat()
        with open(FINDINGS_PATH, "w") as f:
            json.dump(findings, f, indent=2)

        with open(HTML_REPORT, "w") as f:
            html = fullauto_output.get("1.0", "end")
            html_fmt = "<br>".join(html.splitlines())
            f.write(f"<html><body><h2>Full Auto Report</h2><pre>{html_fmt}</pre></body></html>")

        fullauto_log("[+] Full auto mode completed and exported.")

    def fullauto_log(msg):
        fullauto_output.insert("end", msg + "\n")
        fullauto_output.see("end")
        log_to_central(msg)

    def save_profile():
        profile = {
            "recon": recon_toggle.get(),
            "ports": port_toggle.get(),
            "dirs": dir_toggle.get(),
            "plugins": plugin_toggle.get(),
            "exploits": exploit_toggle.get()
        }
        with open(PROFILE_PATH, "w") as f:
            json.dump(profile, f)
        fullauto_log("[+] Auto profile saved.")

    def load_profile():
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                profile = json.load(f)
            recon_toggle.select() if profile.get("recon") else recon_toggle.deselect()
            port_toggle.select() if profile.get("ports") else port_toggle.deselect()
            dir_toggle.select() if profile.get("dirs") else dir_toggle.deselect()
            plugin_toggle.select() if profile.get("plugins") else plugin_toggle.deselect()
            exploit_toggle.select() if profile.get("exploits") else exploit_toggle.deselect()
            fullauto_log("[~] Auto profile loaded.")

    def schedule_auto():
        try:
            delay = int(schedule_entry.get().strip())
            threading.Timer(delay, run_full_auto_mode).start()
            fullauto_log(f"[*] Scheduled full auto mode to run in {delay} seconds.")
        except:
            fullauto_log("[!] Invalid schedule delay.")

    # UI Elements
    ctk.CTkLabel(tab, text="Target URL (e.g. https://example.com)").pack(pady=5)
    global fullauto_url_entry
    fullauto_url_entry = ctk.CTkEntry(tab, width=700)
    fullauto_url_entry.pack()

    global recon_toggle, port_toggle, dir_toggle, plugin_toggle, exploit_toggle
    recon_toggle = ctk.CTkCheckBox(tab, text="Run Recon Phase")
    port_toggle = ctk.CTkCheckBox(tab, text="Run Port Scan Phase")
    dir_toggle = ctk.CTkCheckBox(tab, text="Run Directory Scan Phase")
    plugin_toggle = ctk.CTkCheckBox(tab, text="Scan Plugins & Match CVEs")
    exploit_toggle = ctk.CTkCheckBox(tab, text="Auto-Run Matching Exploits")

    for toggle in [recon_toggle, port_toggle, dir_toggle, plugin_toggle, exploit_toggle]:
        toggle.pack()

    load_profile()

    button_frame = ctk.CTkFrame(tab)
    button_frame.pack(pady=10)
    ctk.CTkButton(button_frame, text="Save Profile", command=save_profile).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Run Now", fg_color="orange", hover_color="darkorange",
                  command=lambda: threading.Thread(target=run_full_auto_mode).start()).pack(side="left", padx=5)

    schedule_frame = ctk.CTkFrame(tab)
    schedule_frame.pack(pady=5)
    ctk.CTkLabel(schedule_frame, text="Schedule (sec):").pack(side="left")
    schedule_entry = ctk.CTkEntry(schedule_frame, width=100)
    schedule_entry.insert(0, "30")
    schedule_entry.pack(side="left", padx=5)
    ctk.CTkButton(schedule_frame, text="Schedule Auto Mode", command=schedule_auto).pack(side="left")

    global fullauto_output
    fullauto_output = ctk.CTkTextbox(tab, height=400, width=800)
    fullauto_output.pack(pady=10)
