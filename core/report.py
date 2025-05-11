# core/report.py
import logging 
import os
from fpdf import FPDF
from datetime import datetime

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_summary():
    """
    Generate a summary report string (for console or logs).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    X_Vector_Pro Report
    -------------------
    Generated: {timestamp}

    Recon:
    - Target scanned with passive methods.

    Scan:
    - Common ports checked. Some may be open.

    Brute Force:
    - Attempted basic username/password combos.

    Exploits:
    - Exploit_01 was executed. Simulated result.

    Summary:
    - No critical vulnerabilities exploited.
    """


def export_txt(scan_data, filename="scan_report.txt"):
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w") as f:
        f.write(format_scan_text(scan_data))
    return path


def export_html(scan_data, filename="scan_report.html"):
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w") as f:
        f.write(format_scan_html(scan_data))
    return path


def export_pdf(scan_data, filename="scan_report.pdf"):
    path = os.path.join(REPORT_DIR, filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    for line in format_scan_text(scan_data).splitlines():
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(path)
    return path


def format_scan_text(scan):
    lines = [
        f"Target: {scan.get('target', 'N/A')}",
        f"Timestamp: {scan.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}",
        "-" * 60,
    ]
    for host in scan.get("summary", []):
        lines.append(f"Host: {host.get('ip', 'unknown')}")
        for port in host.get("ports", []):
            lines.append(f"  - {port}")
        lines.append("")
    return "\n".join(lines)


def format_scan_html(scan):
    html = f"""
    <html><head><title>Scan Report - {scan.get('target', 'Unknown')}</title></head>
    <body><h2>Target: {scan.get('target', 'Unknown')}</h2>
    <p><b>Timestamp:</b> {scan.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p><hr>
    """
    for host in scan.get("summary", []):
        html += f"<h4>Host: {host.get('ip', 'unknown')}</h4><ul>"
        for port in host.get("ports", []):
            html += f"<li>{port}</li>"
        html += "</ul>"
    html += "</body></html>"
    return html


def generate_html_credentials_report(valid_creds, filename="valid_credentials.html"):
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w") as f:
        f.write("<html><head><title>X-Vector Report</title></head><body>")
        f.write("<h2>Valid Credentials</h2><ul>")
        for user, pwd in valid_creds:
            f.write(f"<li>{user}:{pwd}</li>")
        f.write("</ul></body></html>")
    return path
