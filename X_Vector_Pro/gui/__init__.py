# gui package for X-Vector Pro interface
# gui/__init__.py

from .dashboard import Dashboard
from .tabs.brute_tab import BruteTab
from .tabs.recon_tab import ReconTab
from .tabs.scanner_tab import ScannerTab
from .tabs.ids_tab import IDSTab
from .tabs.exploit_tab import ExploitTab
from .tabs.auto_mode_tab import AutoModeTab

__all__ = [
    "Dashboard",
    "BruteTab",
    "ReconTab",
    "ScannerTab",
    "IDSTab",
    "ExploitTab",
    "AutoModeTab"
]
from .dashboard import Dashboard
from .tabs_brute import load_brute_tab
from .tabs_recon import load_recon_tab
from .tabs_scanner import load_scanner_tab
from .tabs_exploits import load_exploit_tab
from .tabs_fullauto import load_fullauto_tab
from .tabs_logs import load_logs_tab
from .tabs_settings import load_settings_tab
from .tabs_findings import load_findings_tab

__all__ = [
    "Dashboard",
    "load_brute_tab",
    "load_recon_tab",
    "load_scanner_tab",
    "load_exploit_tab",
    "load_fullauto_tab",
    "load_logs_tab",
    "load_settings_tab",
    "load_findings_tab"
]
