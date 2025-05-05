# ui/Dashboard.py

import tkinter as tk
from tkinter import ttk
from ui.tabs.auto_tab import AutoTab
from ui.tabs.brute_tab import BruteTab
from ui.tabs.exploits_tab import ExploitsTab
from ui.tabs.reports_tab import ReportsTab
from ui.tabs.logs_tab import LogsTab
from ui.theme import apply_dark_theme
from ui.notifications import ToastManager


class Dashboard:
    """
    The Dashboard class serves as the main interface for the X-Vector Pro application.
    It initializes and manages the application's GUI, including tabbed navigation and notifications.
    """

    def __init__(self):
        """
        Initialize the Dashboard instance with default attributes.
        """
        self.root = None
        self.tab_control = None
        self.toast = ToastManager()
        self.tabs = {}

    def inject(self, root, theme="dark"):
        """
        Inject the root Tkinter window into the Dashboard and initialize the GUI components.

        Args:
            root (tk.Tk): The root Tkinter window instance.
            theme (str): The theme to apply ("dark" or "light"). Defaults to "dark".
        """
        self.root = root
        self.root.title("X-Vector Pro")
        self.root.configure(bg="#1e1e1e" if theme == "dark" else "#ffffff")

        if theme == "dark":
            apply_dark_theme(self.root)
        else:
            self._apply_light_theme()

        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        self._load_tabs()
        self.toast.attach(self.root)

    def _apply_light_theme(self):
        """
        Apply a light theme to the root window. Placeholder for light theme implementation.
        """
        # Implement light theme styling if needed
        pass

    def _load_tabs(self):
        """
        Dynamically loads all the tabs into the dashboard.
        """
        tab_classes = {
            "Auto": AutoTab,
            "Brute": BruteTab,
            "Exploits": ExploitsTab,
            "Reports": ReportsTab,
            "Logs": LogsTab
        }

        for name, cls in tab_classes.items():
            try:
                self.tabs[name] = cls(self.tab_control, self.toast)
                self.tab_control.add(self.tabs[name].frame, text=name)
            except Exception as e:
                print(f"Error loading tab '{name}': {e}")

    def add_tab(self, name, tab_class):
        """
        Dynamically adds a new tab to the dashboard.

        Args:
            name (str): The display name of the tab.
            tab_class (class): The class of the tab to instantiate.
        """
        try:
            self.tabs[name] = tab_class(self.tab_control, self.toast)
            self.tab_control.add(self.tabs[name].frame, text=name)
        except Exception as e:
            print(f"Error adding tab '{name}': {e}")

    def remove_tab(self, name):
        """
        Removes a tab from the dashboard.

        Args:
            name (str): The name of the tab to remove.
        """
        if name in self.tabs:
            tab = self.tabs.pop(name)
            self.tab_control.forget(tab.frame)
        else:
            print(f"Tab '{name}' does not exist.")

    def destroy(self):
        """
        Cleans up resources when the application is closed.
        """
        if self.root:
            self.root.destroy()
        self.toast = None
        self.tabs = {}


if __name__ == "__main__":
    # Standalone testing of the Dashboard class
    root = tk.Tk()
    dashboard = Dashboard()
    dashboard.inject(root)
    root.mainloop()
