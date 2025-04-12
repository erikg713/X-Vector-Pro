# ui/tabs_recon.py
import customtkinter as ctk
import threading, socket, requests, tldextract
from tkinter import messagebox

def load_recon_tab(tab):
    def run_recon():
        target = recon_url_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a target URL.")
            return

        recon_output.delete("0.0", "end")
        recon_output.insert("end", f"[*] Starting recon on {target}...\n")

        try:
            headers = {"User-Agent": "Mozilla/5.0 (X-Vector Recon Bot)"}
            r = requests.get(target, headers=headers, timeout=10)

            recon_output.insert("end", "\n--- Headers ---\n")
            for key, value in r.headers.items():
                recon_output.insert("end", f"{key}: {value}\n")

            if "<title>" in r.text:
                title = r.text.split("<title>")[1].split("</title>")[0].strip()
                recon_output.insert("end", f"\n[*] Title: {title}\n")

            recon_output.insert("end", "\n--- CMS Detection ---\n")
            if "wp-content" in r.text or "/wp-login.php" in r.text:
                recon_output.insert("end", "[+] WordPress Detected\n")
            elif "Joomla!" in r.text:
                recon_output.insert("end", "[+] Joomla Detected\n")
            elif "Drupal" in r.text:
                recon_output.insert("end", "[+] Drupal Detected\n")
            else:
                recon_output.insert("end", "[-] CMS Not Identified\n")

            extracted = tldextract.extract(target)
            base_domain = ".".join(part for part in [extracted.domain, extracted.suffix] if part)
            ip = requests.get(f"https://dns.google/resolve?name={base_domain}&type=A").json()
            if "Answer" in ip:
                ip_addr = ip["Answer"][0]["data"]
                recon_output.insert("end", f"\n[*] IP Address: {ip_addr}\n")

        except Exception as e:
            recon_output.insert("end", f"[!] Recon failed: {e}\n")

    def subdomain_scan():
        domain = recon_url_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "Enter a target domain.")
            return

        recon_output.insert("end", "\n[*] Starting subdomain scan...\n")
        wordlist = ["admin", "dev", "mail", "webmail", "test", "vpn", "portal",
                    "beta", "staging", "api", "cpanel", "dashboard", "internal"]

        extracted = tldextract.extract(domain)
        base_domain = ".".join(part for part in [extracted.domain, extracted.suffix] if part)

        found = 0
        for sub in wordlist:
            subdomain = f"{sub}.{base_domain}"
            try:
                ip = socket.gethostbyname(subdomain)
                recon_output.insert("end", f"[+] Found: {subdomain} -> {ip}\n")
                found += 1
            except socket.gaierror:
                pass

        recon_output.insert("end", f"[*] Subdomain scan complete: {found} found\n" if found else "[-] No subdomains found.\n")

    ctk.CTkLabel(tab, text="Target URL (https://example.com)").pack(pady=5)
    recon_url_entry = ctk.CTkEntry(tab, width=700)
    recon_url_entry.pack()

    ctk.CTkButton(tab, text="Scan Subdomains", command=lambda: threading.Thread(target=subdomain_scan).start()).pack(pady=5)
    ctk.CTkButton(tab, text="Run Recon", command=lambda: threading.Thread(target=run_recon).start()).pack(pady=10)

    recon_output = ctk.CTkTextbox(tab, height=400, width=800)
    recon_output.pack()
