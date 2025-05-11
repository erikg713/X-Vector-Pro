# gui/dashboard.py

from core import logger, configuration
import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        logger.info("Dashboard GUI loaded.")

        stealth_mode = configuration.get("stealth_mode")
        if stealth_mode:
            logger.info("GUI initialized in stealth mode.")
