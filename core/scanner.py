import socket
import requests
from utils.logger import log  # Ensure consistent logging
from fpdf import FPDF

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

def port_scan(host, ports=None):
    """
    Perform a TCP port scan on a target host.

    Args:
        host (str): The target IP or hostname to scan.
        ports (list): List of ports to scan. Defaults to common ports.

    Returns:
        list: A list of strings describing the status of each port.
    """
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


def dirb_scan(base_url, paths=None):
    """
    Perform a simple directory brute-force scan on a target URL.

    Args:
        base_url (str): The base URL to scan.
        paths (list): List of paths to check. Defaults to common paths.

    Returns:
        list: A list of found paths with HTTP 200 status.
    """
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


if __name__ == "__main__":
    # Example usage
    target_host = "127.0.0.1"
    target_url = "http://example.com"

    # Port Scan Example
    scan_results = port_scan(target_host)
    print("\n".join(scan_results))

    # Directory Brute-Force Example
    dirb_results = dirb_scan(target_url)
    print("\n".join(dirb_results))
