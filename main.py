import customtkinter as ctk
from gui.brute_tab import BruteTab
from gui.auto_tab import AutoModeTab
from gui.exploit_tab import ExploitsTab
from gui.reports_tab import ReportsTab
from gui.logs_tab import LogsTab
from utils.splash import show_splash_screen
from utils.settings import load_settings

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1C1C1C")
        self.sidebar.pack(side="left", fill="y")

        # Tab content area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Tab view
        self.tab_view = ctk.CTkTabview(self.content_frame)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.brute_tab = BruteTab(self.tab_view)
        self.auto_tab = AutoModeTab(self.tab_view)
        self.exploit_tab = ExploitsTab(self.tab_view)
        self.reports_tab = ReportsTab(self.tab_view)
        self.logs_tab = LogsTab(self.tab_view)

        self.tab_view.add("Brute Force")
        self.tab_view.tab("Brute Force").configure(content=self.brute_tab)

        self.tab_view.add("Auto Mode")
        self.tab_view.tab("Auto Mode").configure(content=self.auto_tab)

        self.tab_view.add("Exploits")
        self.tab_view.tab("Exploits").configure(content=self.exploit_tab)

        self.tab_view.add("Reports")
        self.tab_view.tab("Reports").configure(content=self.reports_tab)

        self.tab_view.add("Logs")
        self.tab_view.tab("Logs").configure(content=self.logs_tab)

        # Sidebar buttons
        self._add_sidebar_button("Brute Force", "#FF4500", "#FF6347")
        self._add_sidebar_button("Auto Mode", "#007bff", "#0056b3")
        self._add_sidebar_button("Exploits", "#FF4500", "#FF6347")
        self._add_sidebar_button("Reports", "#007bff", "#0056b3")
        self._add_sidebar_button("Logs", "#FF4500", "#FF6347")

    def _add_sidebar_button(self, name, fg_color, hover_color):
        button = ctk.CTkButton(
            self.sidebar,
            text=name,
            command=lambda n=name: self.tab_view.set(n),
            fg_color=fg_color,
            hover_color=hover_color,
            width=180
        )
        button.pack(pady=10, padx=10)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro | Silent. Adaptive. Lethal.")
        self.geometry("1200x800")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        show_splash_screen()
        load_settings()

        DashboardFrame(self)

if __name__ == "__main__":
    MainApp().mainloop()
