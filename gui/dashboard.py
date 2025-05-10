from core import recon

def on_run_recon_clicked():
    target = target_entry.get()
    report = recon.run_auto_recon(target)
    output_textbox.insert("end", report)
import customtkinter as ctk
from gui.widgets import (
    StealthButton,
    DarkModeToggle,
    ToastNotifier,
    LoadingIndicator,
    StatusBar,
    SidebarNav,
    InvisibleWidget,
)

class XVectorDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Layout: sidebar, content, status bar
        self.sidebar = SidebarNav(self, tabs=["AutoMode", "Brute", "Exploits", "Reports", "Settings"], callback=self.switch_tab)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, fg_color="gray12")
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.status_bar = StatusBar(self, text="Ready")

        self.loading = None
        self.build_default_ui()

    def build_default_ui(self):
        # Default tab
        self.switch_tab("AutoMode")

        # Dark mode toggle
        toggle = DarkModeToggle(self.status_bar, command=self.update_theme_status)
        toggle.pack(side="right", padx=10)

        # Stealth trigger zone
        stealth_zone = InvisibleWidget(self, command=lambda: self.popup("Stealth Triggered"))
        stealth_zone.place(x=2, y=2)

    def switch_tab(self, tab_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.status_bar.update_status(f"Switched to {tab_name}")

        if tab_name == "AutoMode":
            label = ctk.CTkLabel(self.content_frame, text="Full Auto Mode Ready", font=("Arial", 24))
            label.pack(pady=50)

            StealthButton(self.content_frame, text="Start Auto Recon", command=lambda: self.popup("Running full recon")).pack(pady=10)
            self.loading = LoadingIndicator(self.content_frame)
            self.loading.pack(pady=20)

        elif tab_name == "Brute":
            label = ctk.CTkLabel(self.content_frame, text="Brute Force Module", font=("Arial", 24))
            label.pack(pady=50)

        elif tab_name == "Exploits":
            label = ctk.CTkLabel(self.content_frame, text="Exploit Arsenal", font=("Arial", 24))
            label.pack(pady=50)

        elif tab_name == "Reports":
            label = ctk.CTkLabel(self.content_frame, text="Scan Reports", font=("Arial", 24))
            label.pack(pady=50)

        elif tab_name == "Settings":
            label = ctk.CTkLabel(self.content_frame, text="Settings Panel", font=("Arial", 24))
            label.pack(pady=50)

    def popup(self, message):
        ToastNotifier(self, message)

    def update_theme_status(self, mode):
        self.status_bar.update_status(f"Theme: {mode.capitalize()}")


if __name__ == "__main__":
    app = XVectorDashboard()
    app.mainloop()
