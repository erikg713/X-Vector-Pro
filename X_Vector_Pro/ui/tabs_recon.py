from gui.recon_viewer import ReconViewer
import customtkinter as ctk

class ReconTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.recon_view = ReconViewer(self)
        self.recon_view.pack(fill="both", expand=True)
