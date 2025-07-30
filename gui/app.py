import sys
import customtkinter as ctk
from gui.tabs.auto_tab import AutoTab
from gui.tabs.scan_tab import ScanTab

class XVectorProApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("X-Vector Pro")
        self.root.geometry("900x600")

        self.tab_view = ctk.CTkTabview(self.root)
        self.tab_view.pack(expand=True, fill="both")

        self.tab_view.add("Auto Mode")
        self.tab_view.add("Scan Plugins")

        self.auto_tab = AutoTab(self.tab_view)
        self.scan_tab = ScanTab(self.tab_view)

        self.tab_view.set("Auto Mode")

        self.auto_tab.pack(expand=True, fill="both")
        self.scan_tab.pack(expand=True, fill="both")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = XVectorProApp()
    app.run()
