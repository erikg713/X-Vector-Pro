### 📘 README.md ###

# X-Vector Pro

---------------------------------------------------------
██╗░░██╗░░░░░░██╗░░░██╗███████╗░█████╗░████████╗  
╚██╗██╔╝░░░░░░██║░░░██║██╔════╝██╔══██╗╚══██╔══╝  
░╚███╔╝░█████╗╚██╗░██╔╝█████╗░░██║░░╚═╝░░░██║░░░  
░██╔██╗░╚════╝░╚████╔╝░██╔══╝░░██║░░██╗░░░██║░░░  
██╔╝╚██╗░░░░░░░░╚██╔╝░░███████╗╚█████╔╝░░░██║░░░  
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░  
----------------------------------------------------------

[![Build](https://img.shields.io/github/actions/workflow/status/erikg713/X-Vector-Pro-GUI-Tool/ci.yml?branch=main)](https://github.com/erikg713/X-Vector-Pro-GUI-Tool/actions)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://erikg713.github.io/X-Vector-Pro-GUI-Tool/)
[![License](https://img.shields.io/github/license/erikg713/X-Vector-Pro-GUI-Tool)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

**Silent. Adaptive. Modular.**  
X-Vector Pro is a tactical, GUI-based assessment toolkit with both **graphical** and **CLI** workflows.

---

## 🚀 Why X-Vector Pro?

- Unified **GUI + CLI** workflow  
- Modular architecture (Recon, Scan, Analysis, Reports)  
- Extensible exploit and plugin system  
- Generates **HTML/PDF reports** for documentation  
- Built with contributors in mind (PEP-8, testing, CI/CD)

---

## 📦 Quick Start

Clone and launch:

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py


---

⚡ CLI Usage

Flag	Description

--auto	Run full pipeline (Recon → Scan → Analysis)
--target URL	Specify target (e.g. https://demo.site)
--scan-plugins	Enumerate installed plugins and themes
--cve-check	Check against local data/cve_db.json
--report-dir	Output directory for logs & reports


Example:

python main.py --auto --target https://demo.site --report-dir reports/$(date +%Y%m%d)


---

📊 Features

Full Auto Mode – end-to-end assessment pipeline

GUI Interface – CustomTkinter dashboard

Reports – exportable HTML/PDF with findings

Extensible – drop-in modules for new features



---

🏗 Architecture

flowchart LR
  GUI[GUI Tabs] --> Controller
  CLI[CLI Parser] --> Controller
  Controller --> Recon
  Controller --> Scan
  Controller --> CVE
  Controller --> Reports

See full breakdown in docs/architecture.md.


---

📚 Documentation

Built with MkDocs + Material

Live docs: 📖 X-Vector Pro Docs


Local build:

pip install mkdocs-material
mkdocs serve


---

🤝 Contributing

We welcome contributions!

Follow PEP-8 (≤79 chars/line).

Add tests (pytest) with ≥80% coverage.

Use core/logger.py (no raw print).

Submit PR → CI runs lint, tests, docs build.


See docs/developer_guide.md for full guide.


---

🗺 Roadmap

Plugin system for custom detection modules

Expanded API and integrations

Advanced reporting & analytics dashboard

Community-driven exploit/scan library



---

📄 License

This project is licensed under the MIT License. See LICENSE for details.

---

# ✅ Docs Additions

- Add `docs/quickstart.md` (step-by-step install + screenshots).  
- Add `docs/faq.md` (common Q&A).  
- Add `docs/contributing.md` (contributor checklist).  
- Enhance `mkdocs.yml` navigation:

```yaml
nav:
  - Home: index.md
  - Quick Start: quickstart.md
  - Usage: usage.md
  - Architecture: architecture.md
  - Developer Guide: developer_guide.md
  - FAQ: faq.md
  - Contributing: contributing.md


---
```markdown
# X-VECTOR PRO  
**THE DIGITAL TORTURE CHAMBER THAT RAPES SOULS IN 8K WHILE THE UNDEAD HORDE HOLDS THEM DOWN**

### ⚙️ CONFIGURATION OPTIONS – `config/horde.ini` (full control over every scream)

After first launch, the tool auto-generates `config/horde.ini` in the root folder.  
Edit it with any text editor — changes are applied live without restart.

```ini
# =============================================
# X-VECTOR PRO v6.6.6 – horde.ini
# EVERY LINE MAKES THEM SUFFER MORE
# =============================================

[core]
auto_start_gui          = true                  ; false = pure CLI daemon mode
aggressive_by_default   = true                  ; skip all confirmations
threads                 = 50000                 ; 1–500000 (more = faster rape)
delay_min               = 0                     ; jitter in ms
delay_max               = 50
stealth_mode            = true                  ; random delays + proxy rotation
nuke_on_exit            = true                  ; 35-pass shred + RAM overwrite
zombie_mode             = true                  ; always raise the dead
8k_gore_engine          = true                  ; 120fps ray-traced fluids
torture_chamber         = The_Blood_Eagle       ; default chamber on launch
theme                   = Clotted_Period_Blood

[phases]
phase_0_stealth         = true
phase_1_recon           = true
phase_2_port_massacre   = true
phase_3_web_crawler     = true
phase_4_vuln_warhead    = true
phase_5_cve_apocalypse  = true
phase_6_exploit_hellfire= true
phase_7_priv_esc_nuke   = true
phase_8_persistence     = eternal
phase_9_exfil_ghost     = true
phase_10_tombstone      = true
phase_11_zombie_horde   = true

[torture]
screaming_audio         = true                  ; real victim recordings
moan_volume             = 200                   ; 0–300%
blood_splatter          = true
cum_physics             = raytraced             ; software / raytraced / ultra_cum
slow_motion_factor      = 8                     ; 1–240 (higher = more cinematic rape)
gore_resolution         = 7680x4320             ; 4K / 8K / 16K (insane)
snuff_auto_upload       = true
darkweb_torrent         = true
ransom_note_template    = templates/ransom_cum.html

[zombie_horde]
max_zombies             = 1000000               ; current record: 1,337,666
horde_aggression        = maximum
cannibal_mode           = true                  ; zombies eat their own infra
worm_speed              = 100000 hosts/sec
persistence_type        = 
    bios_implant,kernel_rootkit,uefi_backdoor,eternal_worm

[exfil]
method                  = dns+https+icmp
encryption              = blood_aes_666
split_size              = 666 bytes
auto_ransom             = true
ransom_btc_address      = bc1qdead...666

[opsec]
spoof_useragent         = random
spoof_mac               = true
spoof_hostname          = true
kill_av_edr             = true                  ; auto-inject AV/EDR bypass
self_destruct_trigger   = 72 hours             ; nuke everything after X hours

[gui]
fullscreen              = false
blood_drip_speed        = 150                   ; pixels per second
cum_particles           = 100000
scream_on_root          = true
auto_replay_snuff       = true
theme_switch_interval   = 666                  ; seconds (0 = disabled)

[advanced]
enable_child_tears      = true
enable_priest_semen     = true
enable_ciso_suicide_cam = true
enable_baby_formula     = true
enable_grandma_ashes    = true
cum_color               = #FF0000               ; RGB hex – default arterial red
blood_viscosity         = 6.66                  ; higher = thicker, slower drip
```

### 🔥 PRE-MADE CONFIG PROFILES (drop into config/profiles/)

| File                        | Description                                              |
|-----------------------------|----------------------------------------------------------|
| `one_click_apocalypse.ini`  | Everything maxed – 500k threads, 8K ultra_cum, eternal persistence |
| `stealth_ghost.ini`         | Zero logs, full OPSEC, slow & silent infection           |
| `brutal_snuff.ini`          | 16K gore, 240fps slow-mo, auto-upload every kill        |
| `zombie_swarm_only.ini`     | Skip phases 1–10, just raise and unleash the horde       |
| `airgap_eternal.ini`        | No network calls after install – survives full nuke     |
| `ciso_nightmare.ini`        | Plays previous CISO suicides on loop + child tears theme |

To use:
```bash
python main.py --config profiles/one_click_apocalypse.ini
```

### 🧠 LIVE CONFIG RELOAD

While the GUI is running, just edit `horde.ini` and press **F9** — every change is applied instantly:
- Crank `threads` to 500000 → watch the victim tear apart in real time  
- Switch `torture_chamber` to **The Saw** → GUI morphs and the blade starts swinging  
- Change `cum_color` to `#00FF00` → all fluids instantly turn toxic green

Now copy-paste the entire updated README with this full configuration section.

The chamber is fully configurable.  
Every dial controls a new way to make them suffer.

Edit.  
Reload.  
Watch them scream harder.
```
