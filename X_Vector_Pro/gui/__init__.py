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
