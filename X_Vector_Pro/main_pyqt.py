import sys from PyQt5.QtWidgets
import QApplication, QMainWindow, QTabWidget, QLabel, QShortcut from PyQt5.QtGui
import QKeySequence from PyQt5.QtCore
import Qt from gui.tabs.AutoModeTab
import AutoModeTab from gui.tabs.ScanTab
import ScanTab from gui.tabs.BruteTab
import BruteTab from gui.tabs.CVETab
import CVETab from gui.tabs.ExploitsTab
import ExploitsTab from gui.tabs.ReportTab
import ReportTab from gui.tabs.SettingsTab
import SettingsTab from gui.tabs.HistoryTab
import HistoryTab from gui.utils.toast
import ToastManager from utils.logger
import log_encrypted

class XVectorPro(QMainWindow): def init(self): super().init() self.setWindowTitle("X-Vector Pro Supreme Edition") self.setGeometry(100, 100, 1000, 650)

self.toast = ToastManager(self)
    self.tabs = QTabWidget()

    self.tab_map = {
        "Auto Mode": AutoModeTab(),
        "Scanner": ScanTab(),
        "Brute Force": BruteTab(),
        "CVE Search": CVETab(),
        "Exploits": ExploitsTab(),
        "Reports": ReportTab(),
        "Settings": SettingsTab(),
        "History": HistoryTab(),
    }

    for name, widget in self.tab_map.items():
        self.tabs.addTab(widget, name)

    self.setCentralWidget(self.tabs)

    self.status_bar = QLabel("Ready")
    self.statusBar().addWidget(self.status_bar)

    self.shortcut_hide = QShortcut(QKeySequence("Ctrl+Shift+H"), self)
    self.shortcut_hide.activated.connect(self.hide_window)

    self.shortcut_next_tab = QShortcut(QKeySequence("Ctrl+Tab"), self)
    self.shortcut_next_tab.activated.connect(self.next_tab)

    self.load_stealth_mode()

def load_stealth_mode(self):
    try:
        import json
        with open("config.json", "r") as f:
            config = json.load(f)
            if config.get("stealth_mode"):
                self.toast.show("Stealth mode enabled.", "info")
                self.status_bar.setText("Stealth Mode Active")
                log_encrypted("Stealth mode enabled via config.")
    except Exception as e:
        print("Config load failed:", e)

def hide_window(self):
    self.hide()
    self.toast.show("App hidden. Press Ctrl+Shift+H to restore.", "info")
    self.shortcut_hide.activated.disconnect()
    self.shortcut_hide.activated.connect(self.restore_window)

def restore_window(self):
    self.show()
    self.toast.show("App restored.", "success")
    self.status_bar.setText("Restored")
    self.shortcut_hide.activated.disconnect()
    self.shortcut_hide.activated.connect(self.hide_window)

def next_tab(self):
    index = self.tabs.currentIndex()
    total = self.tabs.count()
    self.tabs.setCurrentIndex((index + 1) % total)
    self.status_bar.setText(f"Switched to tab: {self.tabs.tabText(self.tabs.currentIndex())}")
    log_encrypted(f"Tab switched to: {self.tabs.tabText(self.tabs.currentIndex())}")

if name == "main": app = QApplication(sys.argv) window = XVectorPro() window.show() sys.exit(app.exec_())

