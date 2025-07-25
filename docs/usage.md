docs/usage.md
markdown
# Usage & Examples

## Installation

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
GUI Walkthrough
Launch python main.py.

Select Auto Mode tab:


Switch to Scan & Enumeration:


Final Report Preview:


CLI Examples
Command	Effect
python main.py --auto --target https://example.com	Full pipeline from recon to exploit + report
python main.py --scan-plugins --target https://demo.wp	Enumerate and version-check plugins/themes
python main.py --cve-check --target https://vuln.site	Detect local CVEs and annotate results in reports
python main.py --auto --target https://test --report-dir r	Custom directory for saving logs & HTML report
Sequence
