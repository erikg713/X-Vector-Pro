ui/tabs_fullauto.py

import customtkinter as ctk import threading, socket, json, re, os, requests, tldextract from utils.logger import log_to_central import importlib.util

def load_fullauto_tab(tab): def run_full_auto_mode(): url = fullauto_url_entry.get().strip() if not url.startswith("http"): fullauto_log("[!] Invalid URL. Use full http/https format.") return

fullauto_log("[*] Starting full auto mode...")

    # Recon
    if recon_toggle.get():
        try:
            fullauto_log("[*] Running Recon...")
            r = requests.get(url, timeout=10)
            if "<title>" in r.text:
                title = r.text.split("<title>")[1].split("</title>")[0].strip()
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
                            fullauto_log(f"    [!!] {plugin} v{version} is vulnerable!")
                            fullauto_log(f"         → {vuln_db[plugin][version]['desc']}")
                            found_plugins.append(vuln_db[plugin][version]['exploit'])
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
                fullauto_log(f"    [+] Result: {result}")
            except Exception as e:
                fullauto_log(f"    [!] Exploit failed: {e}")

    fullauto_log("[*] Full auto mode completed.")

def fullauto_log(msg):
    fullauto_output.insert("end", msg + "\n")
    fullauto_output.see("end")
    log_to_central(msg)

ctk.CTkLabel(tab, text="Target URL (e.g. https://example.com)").pack(pady=5)
fullauto_url_entry = ctk.CTkEntry(tab, width=700)
fullauto_url_entry.pack()

global recon_toggle, port_toggle, dir_toggle, plugin_toggle, exploit_toggle
recon_toggle = ctk.CTkCheckBox(tab, text="Run Recon Phase")
recon_toggle.select()
recon_toggle.pack()

port_toggle = ctk.CTkCheckBox(tab, text="Run Port Scan Phase")
port_toggle.select()
port_toggle.pack()

dir_toggle = ctk.CTkCheckBox(tab, text="Run Directory Scan Phase")
dir_toggle.select()
dir_toggle.pack()

plugin_toggle = ctk.CTkCheckBox(tab, text="Scan Plugins & Match CVEs")
plugin_toggle.select()
plugin_toggle.pack()

exploit_toggle = ctk.CTkCheckBox(tab, text="Auto-Run Matching Exploits")
exploit_toggle.select()
exploit_toggle.pack()

ctk.CTkButton(tab, text="Launch Full Auto Attack Chain",
              fg_color="orange", hover_color="darkorange",
              command=lambda: threading.Thread(target=run_full_auto_mode).start()).pack(pady=20)

global fullauto_output
fullauto_output = ctk.CTkTextbox(tab, height=400, width=800)
fullauto_output.pack(pady=10)

