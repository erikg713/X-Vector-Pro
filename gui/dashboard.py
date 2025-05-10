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

from core import recon, scanner, brute
from core.exploits import runner as exploit_runner

class XVectorDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.sidebar = SidebarNav(self, tabs=["AutoMode", "Brute", "Exploits", "Reports", "Settings"], callback=self.switch_tab)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, fg_color="gray12")
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.status_bar = StatusBar(self, text="Ready")
        self.status_bar.pack(side="bottom", fill="x")

        self.loading = None
        self.build_default_ui()

    def build_default_ui(self):
        self.switch_tab("AutoMode")
        toggle = DarkModeToggle(self.status_bar, command=self.update_theme_status)
        toggle.pack(side="right", padx=10)
        stealth_zone = InvisibleWidget(self, command=lambda: self.popup("Stealth Triggered"))
        stealth_zone.place(x=2, y=2)

    def switch_tab(self, tab_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.status_bar.update_status(f"Switched to {tab_name}")

        if tab_name == "AutoMode":
            label = ctk.CTkLabel(self.content_frame, text="Full Auto Mode Ready", font=("Arial", 24))
            label.pack(pady=10)

            self.target_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter target (e.g., example.com)", width=400)
            self.target_entry.pack(pady=10)

            self.output_box = ctk.CTkTextbox(self.content_frame, width=800, height=350)
            self.output_box.pack(pady=10)

            StealthButton(self.content_frame, text="Run Full Auto Chain", command=self.on_run_full_chain).pack(pady=10)

            self.loading = LoadingIndicator(self.content_frame)
            self.loading.pack(pady=10)

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

    def on_run_full_chain(self):
        target = self.target_entry.get()
        if not target:
            self.popup("Please enter a target.")
            return

        self.status_bar.update_status("Running full auto chain...")
        self.loading.start()
        self.output_box.delete("1.0", "end")

        try:
            self.output_box.insert("end", "[*] Starting Recon...\n")
            recon_result = recon.run_auto_recon(target)
            self.output_box.insert("end", recon_result + "\n")

            self.output_box.insert("end", "[*] Scanning Target...\n")
            scan_result = scanner.run_scan(target)
            self.output_box.insert("end", scan_result + "\n")

            self.output_box.insert("end", "[*] Running Brute Force...\n")
            brute_result = brute.run_brute_force(target)
            self.output_box.insert("end", brute_result + "\n")

            self.output_box.insert("end", "[*] Running Exploit Arsenal...\n")
            exploit_result = exploit_runner.run_all_exploits(target)
            self.output_box.insert("end", exploit_result + "\n")

            self.status_bar.update_status("Full Auto Chain Completed.")
            self.popup("All modules completed successfully.")

        except Exception as e:
            self.output_box.insert("end", f"[ERROR] {str(e)}\n")
            self.status_bar.update_status("Error in Auto Chain.")
            self.popup(f"Error: {str(e)}")

        finally:
            self.loading.stop()


if __name__ == "__main__":
    app = XVectorDashboard()
    app.mainloop()
