ui/tabs_fullauto.py

import customtkinter as ctk import threading, socket, json, re, os, requests, tldextract from utils.logger import log_to_central import importlib.util import time import datetime

PROFILE_PATH = "auto_profile.json" FINDINGS_PATH = "fullauto_findings.json" HTML_REPORT = "fullauto_report.html"

def load_fullauto_tab(tab): def run_full_auto_mode(): url = fullauto_url_entry.get().strip() if not url.startswith("http"): fullauto_log("[!] Invalid URL. Use full http/https format.") return

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
            r = requests.get(url, timeout=10)
            if "<title>" in r.text:
                title = r.text.split("<title>")[1].split("</title>")[0].strip()
                findings["title"] = title
                fullauto_log(f"    [+] Site title: {title}")
        except Exception as e:
            fullauto_log(f"[!] Recon failed: {e}")

    # Port Scan
    if port_toggle.get():
        try:
            fullauto_log("[*] Running Port Scan...")
            target_host = tldextract.extract(url).registered_domain
            ip = socket.gethostbyname(target_host)
            for port in [21, 22, 80, 443, 3306]:
                try:
                    s = socket.socket()
                    s.settimeout(0.3)
                    if s.connect_ex((ip, port)) == 0:
                        findings["open_ports"].append(port)
                        fullauto_log(f"    [+] Open port: {port}")
                    s.close()
                except:
                    continue
        except Exception as e:
            fullauto_log(f"[!] Port scan failed: {e}")

    # Directory Scan
    if dir_toggle.get():
        try:
            fullauto_log("[*] Running Dir Scan...")
            common_dirs = ["admin", "login", "wp-admin", "config"]
            for d in common_dirs:
                check = f"{url.rstrip('/')}/{d}"
                try:
                    resp = requests.get(check, timeout=3)
                    if resp.status_code in [200, 301, 403]:
                        findings["directories"].append({"path": check, "code": resp.status_code})
                        fullauto_log(f"    [+] Found: {check} ({resp.status_code})")
                except:
                    continue
        except Exception as e:
            fullauto_log(f"[!] Dir scan failed: {e}")

    # Plugin Detection + CVE Match
    found_plugins = []
    if plugin_toggle.get():
        try:
            fullauto_log("[*] Checking for plugins/themes...")
            r = requests.get(url, timeout=10)
            html = r.text
            with open("cve_db.json") as f:
                vuln_db = json.load(f)

            for plugin in vuln_db:
                if f"/wp-content/plugins/{plugin}" in html:
                    version_match = re.search(rf'/wp-content/plugins/{plugin}.*?[?&]ver=([0-9\.]+)', html)
                    if version_match:
                        version = version_match.group(1)
                        if version in vuln_db[plugin]:
                            cve = vuln_db[plugin][version]
                            findings["cves"].append({"plugin": plugin, "version": version, "cve": cve["cve"], "desc": cve["desc"]})
                            fullauto_log(f"    [!!] {plugin} v{version} is vulnerable!")
                            fullauto_log(f"         → {cve['desc']}")
                            found_plugins.append(cve["exploit"])
            if not found_plugins:
                fullauto_log("    [-] No known vulnerable plugins found.")
        except Exception as e:
            fullauto_log(f"[!] Plugin check failed: {e}")
            return

    # Exploits
    if exploit_toggle.get():
        for exploit in found_plugins:
            fullauto_log(f"[*] Launching exploit: {exploit}")
            try:
                path = os.path.join("exploits", f"{exploit}.py")
                spec = importlib.util.spec_from_file_location(exploit, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                result = mod.run(url)
                findings["exploits"].append({"exploit": exploit, "result": result})
                fullauto_log(f"    [+] Result: {result}")
            except Exception as e:
                findings["exploits"].append({"exploit": exploit, "result": str(e)})
                fullauto_log(f"    [!] Exploit failed: {e}")

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
        if profile.get("recon"): recon_toggle.select()
        else: recon_toggle.deselect()
        if profile.get("ports"): port_toggle.select()
        else: port_toggle.deselect()
        if profile.get("dirs"): dir_toggle.select()
        else: dir_toggle.deselect()
        if profile.get("plugins"): plugin_toggle.select()
        else: plugin_toggle.deselect()
        if profile.get("exploits"): exploit_toggle.select()
        else: exploit_toggle.deselect()
        fullauto_log("[~] Auto profile loaded.")

def schedule_auto():
    try:
        delay = int(schedule_entry.get().strip())
        threading.Timer(delay, run_full_auto_mode).start()
        fullauto_log(f"[*] Scheduled full auto mode to run in {delay} seconds.")
    except:
        fullauto_log("[!] Invalid schedule delay.")

ctk.CTkLabel(tab, text="Target URL (e.g. https://example.com)").pack(pady=5)
fullauto_url_entry = ctk.CTkEntry(tab, width=700)
fullauto_url_entry.pack()

global recon_toggle, port_toggle, dir_toggle, plugin_toggle, exploit_toggle
recon_toggle = ctk.CTkCheckBox(tab, text="Run Recon Phase")
recon_toggle.pack()
port_toggle = ctk.CTkCheckBox(tab, text="Run Port Scan Phase")
port_toggle.pack()
dir_toggle = ctk.CTkCheckBox(tab, text="Run Directory Scan Phase")
dir_toggle.pack()
plugin_toggle = ctk.CTkCheckBox(tab, text="Scan Plugins & Match CVEs")
plugin_toggle.pack()
exploit_toggle = ctk.CTkCheckBox(tab, text="Auto-Run Matching Exploits")
exploit_toggle.pack()

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

