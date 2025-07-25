## GUI Walkthrough

1. Launch `python main.py`.  
2. Select **Auto Mode** tab:  
   ![Auto Mode Tab](img/auto_mode_tab.png)

3. Switch to **Scan & Enumeration**:  
   ![Scan Tab](img/scan_tab.png)

4. Final **Report Preview**:  
   ![Report Preview](img/report_preview.png)

sequenceDiagram
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

