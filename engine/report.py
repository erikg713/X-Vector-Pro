import json

class ReportGenerator:
    def __init__(self, html_output, logger):
        self.html_output = html_output
        self.log = logger

    def write(self, findings, json_path="fullauto_findings.json", html_path="fullauto_report.html"):
        with open(json_path, "w") as f:
            json.dump(findings, f, indent=2)

        html = self.html_output.get("1.0", "end")
        formatted = "<br>".join(html.splitlines())
        with open(html_path, "w") as f:
            f.write(f"<html><body><h2>Full Auto Report</h2><pre>{formatted}</pre></body></html>")

        self.log(f"[+] Exported findings and HTML report.")
