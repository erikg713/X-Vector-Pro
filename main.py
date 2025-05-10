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

def launch_gui():
    app = XVectorGUI()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()
