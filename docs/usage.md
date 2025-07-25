# Usage & Examples #

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

### Sequence Diagram ###
  participant U as User
  participant GUI
  participant CLI
  participant C as Controller
  participant R as Recon
  participant S as Scan
  participant B as Brute
  participant V as CVE
  participant E as Exploit
  participant P as Reports

  U->>GUI: Click “Auto Mode”  
  U->>CLI: python main.py --auto --target URL  
  GUI-->>C: start_auto()  
  CLI-->>C: parse_args()  

  C->>R: run_recon(target)  
  R-->>C: recon_data  

  C->>S: run_scan(target)  
  S-->>C: scan_data  

  C->>B: run_brute(target)  
  B-->>C: creds  

  C->>V: run_cve_check(target)  
  V-->>C: cve_list  

  C->>E: execute_all(findings)  
  E-->>C: exploit_results  

  C->>P: generate_report(results)  
  P-->>U: HTML/PDF in `reports/DATE`
