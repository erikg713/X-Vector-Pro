#### GUI-BRUTEFORCE-TOOL ####

# X-Vector Pro

**Silent. Adaptive. Lethal.**  
X-Vector Pro is an advanced penetration testing toolkit with modular scanning, CVE discovery, and custom exploit automation — all in one GUI.

## Features

- Full Auto Mode (Recon → Scan → Plugin Check → Exploit)
- WordPress brute force (XML-RPC)
- CVE detection via local `cve_db.json`
- Plugin/theme enumeration
- Exploit runner from `exploits/` folder
- Tab-based GUI (CustomTkinter)
- Findings management and export
- HTML report & log generation

## Tech Stack

- Python 3.9+
- CustomTkinter
- Requests
- TLDExtract
- XML-RPC
- JSON, Regex, Sockets

## Getting Started

```bash
git clone https://github.com/your-username/x-vector-pro.git
cd x-vector-pro
pip install -r requirements.txt
python main.py

Project Structure

x_vector_pro/
├── main.py
├── ui/
├── engine/
├── utils/
├── exploits/
├── data/
├── README.md
├── .gitignore
└── requirements.txt

To-Do
tests####
[ ] Add REST API support

[ ] Add exploit editor GUI

[ ] CVE auto-updater

[ ] Multi-threaded scan orchestration


License

MIT License

---

