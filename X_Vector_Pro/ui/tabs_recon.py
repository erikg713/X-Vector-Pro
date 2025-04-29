import customtkinter as ctk
from gui.recon_viewer import ReconViewer

class ReconTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Header section with a blue background color and padding
        header_frame = ctk.CTkFrame(self, height=50, corner_radius=10, bg_color="#007BFF")  # Blue color
        header_frame.pack(fill="x", pady=(10, 5))

        # Title label inside the header with white text
        title_label = ctk.CTkLabel(header_frame, text="Recon Viewer", font=("Roboto", 20, "bold"), fg="#FFFFFF")
        title_label.pack(pady=10)

        # ReconViewer section
        self.recon_view = ReconViewer(self)
        self.recon_view.pack(fill="both", expand=True, padx=10, pady=10)

        # Refresh Button with green color and hover effect
        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh_recon, font=("Roboto", 14), fg_color="#28A745", hover_color="#218838")  # Green color
        self.refresh_button.pack(pady=15)

        # Tooltip for the refresh button
        self.refresh_button.bind("<Enter>", lambda e: self.show_tooltip("Refresh Recon Data"))
        self.refresh_button.bind("<Leave>", lambda e: self.hide_tooltip())

        # Tooltip label (initially hidden)
        self.tooltip_label = ctk.CTkLabel(self, text="", font=("Roboto", 10), fg="#FFFFFF", bg_color="#007BFF")  # Blue background for tooltip
        self.tooltip_label.pack_forget()

        # Loading Spinner (hidden initially)
        self.loading_spinner = ctk.CTkProgressBar(self, mode="indeterminate", width=200, height=5)
        self.loading_spinner.pack(pady=10)
        self.loading_spinner.set(0)
        self.loading_spinner.grid_forget()

    def refresh_recon(self):
        # Show loading spinner
        self.loading_spinner.grid(row=2, column=0, pady=10)

        # Logic to refresh recon data (you could call a method in ReconViewer)
        print("Refreshing Recon...")

        # Simulate a delay for loading data
        self.after(2000, self.update_recon)

    def update_recon(self):
        # Hide loading spinner after data is refreshed
        self.loading_spinner.grid_forget()
        print("Recon data refreshed!")

        # You can update the recon viewer's data here
        self.recon_view.update_data()

    def show_tooltip(self, text):
        self.tooltip_label.config(text=text)
        self.tooltip_label.place(x=self.refresh_button.winfo_x() + 50, y=self.refresh_button.winfo_y() - 30)

    def hide_tooltip(self):
        self.tooltip_label.pack_forget()
