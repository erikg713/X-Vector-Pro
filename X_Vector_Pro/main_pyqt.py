# main_pyqt.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from gui.tabs.AutoModeTab import AutoModeTab
from gui.tabs.ScanTab import ScanTab
from gui.tabs.BruteTab import BruteTab
from gui.tabs.CVETab import CVETab
from gui.tabs.ExploitsTab import ExploitsTab
from gui.tabs.ReportTab import ReportTab
from gui.tabs.SettingsTab import SettingsTab
from gui.tabs.HistoryTab import HistoryTab

class XVectorPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("X_Vector_Pro")
        self.setGeometry(100, 100, 900, 600)
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()
        tabs.addTab(AutoModeTab(), "Auto Mode")
        tabs.addTab(ScanTab(), "Scanner")
        tabs.addTab(BruteTab(), "Brute Force")
        tabs.addTab(CVETab(), "CVE Search")
        tabs.addTab(ExploitsTab(), "Exploits")
        tabs.addTab(ReportTab(), "Reports")
        tabs.addTab(SettingsTab(), "Settings")
        tabs.addTab(HistoryTab(), "History")

        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XVectorPro()
    window.show()
    sys.exit(app.exec_())
