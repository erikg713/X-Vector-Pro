# gui/widgets/loading_indicator.py
import customtkinter as ctk

class LoadingIndicator(ctk.CTkProgressBar):
    def __init__(self, master):
        super().__init__(master, mode="indeterminate")
        self.start()

    def stop_loading(self):
        self.stop()
