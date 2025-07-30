import sys
import customtkinter as ctk
from gui.tabs.auto_tab import AutoTab
from gui.tabs.scan_tab import ScanTab
from PyQt5.QtWidgets import QApplication, QMainWindow
from core.tabs import MainTabs

class XVectorProApp:
    """
    Wrapper for QApplication and main window with tabs.
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("X-Vector Pro GUI Tool")
        self.main_window.setCentralWidget(MainTabs())
        self.main_window.resize(800, 600)

    def run(self):
        self.main_window.show()
        return self.app.exec_()

class XVectorProApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("X-Vector Pro")
        self.root.geometry("900x600")

        self.tab_view = ctk.CTkTabview(self.root)
        self.tab_view.pack(expand=True, fill="both")

        self.auto_tab = AutoTab(self.tab_view)
        self.scan_tab = ScanTab(self.tab_view)

        self.tab_view.add("Auto Mode")
        self.tab_view.add("Scan Plugins")

        self.tab_view.set("Auto Mode")

        self.auto_tab.pack(expand=True, fill="both")
        self.scan_tab.pack(expand=True, fill="both")

    def run(self):
        self.root.mainloop()
