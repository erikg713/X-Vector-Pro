import customtkinter as ctk
from gui.brute_tab import BruteTab 

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Tab View
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=20)

        # Brute Force Tab
        self.brute_tab = BruteTab(self.tab_view)
        self.tab_view.add("Brute Force")
        self.brute_tab.pack(fill="both", expand=True)
        self.tab_view.tab("Brute Force").configure(content=self.brute_tab)

        # Add more tabs here (e.g., Exploits, AutoMode, Logs)
        # self.exploits_tab = ExploitsTab(self.tab_view)
        # self.tab_view.add("Exploits")
        # self.exploits_tab.pack(fill="both", expand=True)
        # self.tab_view.tab("Exploits").configure(content=self.exploits_tab)
