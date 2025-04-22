import customtkinter as ctk
import tkinter.filedialog as fd
from pymongo import MongoClient
import threading
from core.report import export_txt, export_html, export_pdf
from core.recon.recon_engine import run_auto_recon
from core.ids import suricata_manager, auto_analyzer
from utils.logger import log
import datetime
from gui.tabs.brute_tab import BruteTab  # import the new tab

class Dashboard(ctk.CTk):  # or your main app window
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1100x700")
        self.sidebar()
        self.tab_area()

    def sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=180)
        self.sidebar_frame.pack(side="left", fill="y")

        self.btn_brute = ctk.CTkButton(self.sidebar_frame, text="Brute Force", command=self.show_brute_tab)
        self.btn_brute.pack(pady=(10, 5), fill="x")

        # Add other sidebar buttons here...

    def tab_area(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.current_tab = None

    def clear_tab(self):
        if self.current_tab:
            self.current_tab.destroy()

    def show_brute_tab(self):
        self.clear_tab()
        self.current_tab = BruteTab(self.content_frame)
        self.current_tab.pack(fill="both", expand=True)

class Toast(ctk.CTkToplevel):
    def __init__(self, master, message, duration=2000):
        super().__init__(master)
        self.overrideredirect(True)
        self.geometry(f"250x40+{master.winfo_x() + 30}+{master.winfo_y() + 30}")
        self.configure(fg_color="#2e2e2e")

        label = ctk.CTkLabel(self, text=message, text_color="white")
        label.pack(padx=10, pady=5)
        self.after(duration, self.destroy)


def show_toast(master, message):
    Toast(master, message)


def launch_ids():
    if not suricata_manager.is_running():
        suricata_manager.start_suricata()
    alerts = auto_analyzer.check_for_threats()
    for a in alerts:
        print(f"[ALERT] {a['timestamp']} - {a['alert']}")


class XVectorDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("X-Vector Pro Dashboard")
        self.geometry("1100x720")
        self.resizable(False, False)

        self.build_gui()

    def build_gui(self):
        self.sidebar = ctk.CTkFrame(self, width=180, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="X-Vector Pro", font=("Arial", 20, "bold")).pack(pady=20)

        self.entry = ctk.CTkEntry(self.sidebar, placeholder_text="Enter target...")
        self.entry.pack(padx=10, pady=10)

        ctk.CTkButton(self.sidebar, text="Run Auto Recon", command=self.run_recon_threaded).pack(padx=10, pady=10)

        self.loader = ctk.CTkLabel(self.sidebar, text="")
        self.loader.pack(pady=5)

        self.recon_view = ReconViewer(self)
        self.recon_view.pack(side="right", fill="both", expand=True)

    def run_recon_threaded(self):
        target = self.entry.get().strip()
        if not target:
            show_toast(self, "Enter a valid target")
            return

        self.loader.configure(text="Running recon...")
        threading.Thread(target=self.run_recon, args=(target,), daemon=True).start()

    def run_recon(self, target):
        try:
            log(f"[GUI] Running recon on {target}")
            run_auto_recon(target)
            self.recon_view.load_all()
            show_toast(self, "Recon completed successfully!")
        except Exception as e:
            show_toast(self, f"Error: {str(e)}")
        finally:
            self.loader.configure(text="")


class ReconViewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["xvector"]
        self.col = self.db["auto_recon"]
        self.last_results = []
        self.build_ui()

    def build_ui(self):
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=10, pady=(10, 0))

        self.search_entry = ctk.CTkEntry(top, placeholder_text="Search by IP or timestamp...")
        self.search_entry.pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkButton(top, text="Search", command=self.search).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Load All", command=self.load_all).pack(side="left", padx=5)

        self.filter_open = ctk.CTkCheckBox(top, text="Open Ports Only", command=self.apply_filter)
        self.filter_open.pack(side="left", padx=5)

        self.result_box = ctk.CTkTextbox(self, wrap="word", font=("Courier", 12))
        self.result_box.pack(expand=True, fill="both", padx=10, pady=10)

        export_frame = ctk.CTkFrame(self)
        export_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(export_frame, text="Export TXT", command=self.export_txt).pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="Export HTML", command=self.export_html).pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="Export PDF", command=self.export_pdf).pack(side="left", padx=5)

    def display(self, data):
        self.result_box.delete("1.0", "end")
        if not data:
            self.result_box.insert("end", "No results found.\n")
            return

        for scan in data:
            self.result_box.insert("end", f"[{scan['timestamp']}] Target: {scan['target']}\n")
            for host in scan.get("summary", []):
                self.result_box.insert("end", f"  Host: {host['ip']}\n")
                for port in host["ports"]:
                    self.result_box.insert("end", f"    - {port}\n")
            self.result_box.insert("end", "-"*60 + "\n")

        self.last_results = data

    def search(self):
        term = self.search_entry.get().strip()
        if not term:
            return
        q = {"$or": [
            {"target": {"$regex": term, "$options": "i"}},
            {"timestamp": {"$regex": term, "$options": "i"}}
        ]}
        data = list(self.col.find(q).sort("timestamp", -1))
        self.display(data)

    def load_all(self):
        data = list(self.col.find().sort("timestamp", -1))
        self.display(data)

    def apply_filter(self):
        if not self.last_results:
            return
        show_open_only = self.filter_open.get()
        filtered = []

        for scan in self.last_results:
            filtered_hosts = []
            for host in scan["summary"]:
                open_ports = [p for p in host["ports"] if not show_open_only or "open" in p]
                if open_ports:
                    filtered_hosts.append({"ip": host["ip"], "ports": open_ports})
            if filtered_hosts:
                filtered.append({
                    "target": scan["target"],
                    "timestamp": scan["timestamp"],
                    "summary": filtered_hosts
                })

        self.display(filtered)

    def export_txt(self):
        if not self.last_results:
            return
        file = fd.asksaveasfilename(defaultextension=".txt")
        if file:
            export_txt(self.last_results[0], file)

    def export_html(self):
        if not self.last_results:
            return
        file = fd.asksaveasfilename(defaultextension=".html")
        if file:
            export_html(self.last_results[0], file)

    def export_pdf(self):
        if not self.last_results:
            return
        file = fd.asksaveasfilename(defaultextension=".pdf")
        if file:
            export_pdf(self.last_results[0], file)
# gui/dashboard.py

import customtkinter as ctk
from gui.tabs.brute_tab import BruteTab
from gui.tabs.recon_tab import ReconTab
from gui.tabs.scanner_tab import ScannerTab
from gui.tabs.ids_tab import IDSTab
from gui.tabs.exploit_tab import ExploitTab
from gui.tabs.auto_mode_tab import AutoModeTab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1200x800")
        self.minsize(1024, 700)

        self.active_tab = None
        self.frames = {}
        self.build_layout()

    def build_layout(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="X-Vector Pro", font=("Segoe UI", 20, "bold")).pack(pady=20)

        # Sidebar buttons
        self.add_nav_button("AutoMode", AutoModeTab)
        self.add_nav_button("Brute", BruteTab)
        self.add_nav_button("Recon", ReconTab)
        self.add_nav_button("Scanner", ScannerTab)
        self.add_nav_button("IDS", IDSTab)
        self.add_nav_button("Exploits", ExploitTab)

        # Topbar
        self.topbar = ctk.CTkFrame(self, height=50)
        self.topbar.grid(row=0, column=1, sticky="new")
        self.topbar.grid_propagate(False)

        self.tab_title = ctk.CTkLabel(self.topbar, text="Dashboard", font=("Segoe UI", 18, "bold"))
        self.tab_title.pack(side="left", padx=15)

        # Main content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Load first tab
        self.switch_tab("AutoMode", AutoModeTab)

    def add_nav_button(self, name, frame_class):
        btn = ctk.CTkButton(self.sidebar, text=name, command=lambda: self.switch_tab(name, frame_class))
        btn.pack(fill="x", padx=10, pady=4)

    def switch_tab(self, name, frame_class):
        self.tab_title.configure(text=name)

        if self.active_tab:
            self.frames[self.active_tab].pack_forget()

        if name not in self.frames:
            self.frames[name] = frame_class(self.main_frame)
        self.frames[name].pack(fill="both", expand=True)

        self.active_tab = name
