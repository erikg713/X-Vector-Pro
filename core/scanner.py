import socket
import requests
import os
from datetime import datetime
from utils.logger import log  # Ensure consistent logging
from fpdf import FPDF

# Report directory setup
REPORT_DIR = "reports"
if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)

# Styled PDF class
class StyledPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "X-Vector Pro Scan Report", border=False, ln=True, align="C")
        self.ln(5)
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# Export PDF function
def export_pdf(scan_data, filename="scan_report.pdf"):
    path = os.path.join(REPORT_DIR, filename)
    pdf = StyledPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    # Meta section
    pdf.set_text_color(0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Target: {scan_data.get('target', 'N/A')}", ln=True)
    pdf.cell(0, 10, f"Timestamp: {scan_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", ln=True)
    pdf.ln(5)

    # Host summaries
    pdf.set_font("Arial", size=11)
    for host in scan_data.get("summary", []):
        pdf.set_fill_color(240, 240, 240)
        pdf.set_text_color(0)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, f"Host: {host.get('ip', 'unknown')}", ln=True, fill=True)
        pdf.set_font("Arial", "", 11)
        for port in host.get("ports", []):
            pdf.cell(0, 8, f"  - Port {port}", ln=True)
        pdf.ln(2)

    pdf.output(path)
    return path

# Configuration
DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389, 8080]
DEFAULT_DIRB_PATHS = ["admin", "wp-login", "phpmyadmin"]

# Port scan function
def port_scan(host, ports=None):
    if ports is None:
        ports = DEFAULT_PORTS

    log(f"[*] Starting port scan on {host}")
    results = []

    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=1):
                results.append(f"[+] Port {port} is OPEN")
                log(f"[+] Port {port} is OPEN")
        except Exception as e:
            results.append(f"[-] Port {port} is closed or filtered ({e})")
            log(f"[-] Port {port} is closed or filtered ({e})")

    return results

# Directory brute-force scan
def dirb_scan(base_url, paths=None):
    if paths is None:
        paths = DEFAULT_DIRB_PATHS

    log(f"[*] Starting directory brute-force scan on {base_url}")
    results = []

    for path in paths:
        try:
            url = f"{base_url}/{path}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results.append(f"[+] Found: {url}")
                log(f"[+] Found: {url}")
        except Exception as e:
            log(f"[!] Error accessing {url}: {e}")

    return results

# Example usage
if __name__ == "__main__":
    target_host = "127.0.0.1"
    target_url = "http://example.com"

    # Port Scan Example
    scan_results = port_scan(target_host)
    print("\n".join(scan_results))

    # Directory Brute-Force Example
    dirb_results = dirb_scan(target_url)
    print("\n".join(dirb_results))

    # Sample scan data for report generation
    scan_data = {
        'target': target_host,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'summary': [
            {'ip': '127.0.0.1', 'ports': [80, 443, 8080]},
            {'ip': '192.168.1.1', 'ports': [22, 25, 53]}
        ]
    }

    # Export PDF
    pdf_path = export_pdf(scan_data)
    print(f"PDF Report generated at: {pdf_path}")
