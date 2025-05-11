import customtkinter as ctk
from gui.tabs import init_tabs
from utils.splash import show_splash_screen
from utils.settings import load_settings

class XVectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro | Silent. Adaptive. Lethal.")
        self.geometry("1024x700")

        # Appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Splash screen
        show_splash_screen()

        # Create Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, height=700, corner_radius=0, fg_color="#1C1C1C")
        self.sidebar.pack(side="left", fill="y")

        # Add buttons to Sidebar with blue and orange colors
        self.recon_button = ctk.CTkButton(self.sidebar, text="Recon", command=self.switch_to_recon, 
                                          fg_color="#007bff", hover_color="#0056b3", width=200)
        self.recon_button.pack(pady=10, padx=10, fill="x")

        self.brute_button = ctk.CTkButton(self.sidebar, text="Brute Force", command=self.switch_to_brute, 
                                          fg_color="#FF4500", hover_color="#FF6347", width=200)
        self.brute_button.pack(pady=10, padx=10, fill="x")

        self.exploit_button = ctk.CTkButton(self.sidebar, text="Exploit", command=self.switch_to_exploit, 
                                            fg_color="#007bff", hover_color="#0056b3", width=200)
        self.exploit_button.pack(pady=10, padx=10, fill="x")

        self.report_button = ctk.CTkButton(self.sidebar, text="Reports", command=self.switch_to_reports, 
                                           fg_color="#FF4500", hover_color="#FF6347", width=200)
        self.report_button.pack(pady=10, padx=10, fill="x")

        # Create the main content area for tabs
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Main tab view
        self.tabs = ctk.CTkTabview(self.content_frame, width=980, height=640)
        self.tabs.pack(padx=10, pady=10)
import customtkinter as ctk from gui.brute_tab import BruteTab from gui.auto_tab import AutoModeTab from gui.exploit_tab import ExploitsTab from gui.reports_tab import ReportsTab from gui.logs_tab import LogsTab

class DashboardFrame(ctk.CTkFrame): def init(self, parent): super().init(parent) self.pack(fill="both", expand=True)

# Tab View
    self.tab_view = ctk.CTkTabview(self)
    self.tab_view.pack(fill="both", expand=True, padx=20, pady=20)

    # Brute Force Tab
    self.brute_tab = BruteTab(self.tab_view)
    self.tab_view.add("Brute Force")
    self.brute_tab.pack(fill="both", expand=True)
    self.tab_view.tab("Brute Force").configure(content=self.brute_tab)

    # Auto Mode Tab
    self.auto_tab = AutoModeTab(self.tab_view)
    self.tab_view.add("Auto Mode")
    self.auto_tab.pack(fill="both", expand=True)
    self.tab_view.tab("Auto Mode").configure(content=self.auto_tab)

    # Exploits Tab
    self.exploits_tab = ExploitsTab(self.tab_view)
    self.tab_view.add("Exploits")
    self.exploits_tab.pack(fill="both", expand=True)
    self.tab_view.tab("Exploits").configure(content=self.exploits_tab)

    # Reports Tab
    self.reports_tab = ReportsTab(self.tab_view)
    self.tab_view.add("Reports")
    self.reports_tab.pack(fill="both", expand=True)
    self.tab_view.tab("Reports").configure(content=self.reports_tab)

    # Logs Tab
    self.logs_tab = LogsTab(self.tab_view)
    self.tab_view.add("Logs")
    self.logs_tab.pack(fill="both", expand=True)
    self.tab_view.tab("Logs").configure(content=self.logs_tab)

class MainApp(ctk.CTk): def init(self): super().init() self.title("X-Vector Pro") self.geometry("1200x800") DashboardFrame(self)

if name == "main": ctk.set_appearance_mode("dark") ctk.set_default_color_theme("blue") MainApp().mainloop()


        # Load settings and init tabs
        settings = load_settings()
        init_tabs(self.tabs, self)

    def switch_to_recon(self):
        # Logic for switching to the "Recon" tab
        self.tabs.set("Recon")

    def switch_to_brute(self):
        # Logic for switching to the "Brute Force" tab
        self.tabs.set("Brute")

    def switch_to_exploit(self):
        # Logic for switching to the "Exploit" tab
        self.tabs.set("Exploit")

    def switch_to_reports(self):
        # Logic for switching to the "Reports" tab
        self.tabs.set("Reports")
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1000x700")
        DashboardFrame(self)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    MainApp().mainloop()
