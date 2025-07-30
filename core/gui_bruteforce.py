# core/gui_bruteforce.py
import os
import threading
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QSpinBox, QTextEdit, QProgressBar, QFileDialog, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, QObject
from core.brute import BruteForcer
from config import WORDLIST_DIR

# --- Helper class to emit logs back into the GUI thread ---
class LoggerEmitter(QObject):
    log = pyqtSignal(str)
    progress = pyqtSignal(int, int)  # done, total

class BruteForceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.logger = LoggerEmitter()
        self.logger.log.connect(self._append_log)
        self.logger.progress.connect(self._update_progress)
        self.worker = None

    def _build_ui(self):
        grid = QGridLayout(self)

        # Target URL
        grid.addWidget(QLabel("Target URL:"), 0, 0)
        self.url_edit = QLineEdit("https://example.com/login")
        grid.addWidget(self.url_edit, 0, 1, 1, 2)

        # Userlist
        grid.addWidget(QLabel("Usernames File:"), 1, 0)
        self.user_edit = QLineEdit("usernames.txt")
        btn_u = QPushButton("…")
        btn_u.clicked.connect(self._pick_userlist)
        grid.addWidget(self.user_edit, 1, 1)
        grid.addWidget(btn_u, 1, 2)

        # Passlist
        grid.addWidget(QLabel("Passwords File:"), 2, 0)
        self.pwd_edit = QLineEdit("rockyou.txt")
        btn_p = QPushButton("…")
        btn_p.clicked.connect(self._pick_passlist)
        grid.addWidget(self.pwd_edit, 2, 1)
        grid.addWidget(btn_p, 2, 2)

        # Threads
        grid.addWidget(QLabel("Threads:"), 3, 0)
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 100)
        self.thread_spin.setValue(10)
        grid.addWidget(self.thread_spin, 3, 1)

        # Tor
        grid.addWidget(QLabel("Use Tor:"), 3, 2)
        self.tor_check = QCheckBox()
        grid.addWidget(self.tor_check, 3, 3)

        # Start / Stop buttons
        self.start_btn = QPushButton("Start")
        self.stop_btn  = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.start_btn.clicked.connect(self._on_start)
        self.stop_btn.clicked.connect(self._on_stop)
        grid.addWidget(self.start_btn, 4, 1)
        grid.addWidget(self.stop_btn, 4, 2)

        # Progress bar & log
        self.progress = QProgressBar()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        grid.addWidget(self.progress, 5, 0, 1, 4)
        grid.addWidget(self.log_area, 6, 0, 5, 4)

    def _pick_userlist(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Usernames File",
                                              WORDLIST_DIR, "Text files (*.txt)")
        if path:
            self.user_edit.setText(os.path.basename(path))

    def _pick_passlist(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Passwords File",
                                              WORDLIST_DIR, "Text files (*.txt)")
        if path:
            self.pwd_edit.setText(os.path.basename(path))

    def _on_start(self):
        self.start_btn.setEnabled(False)
        self.stop_btn .setEnabled(True)
        self.log_area.clear()

        # Spawn worker thread
        def target():
            users = self.user_edit.text()
            pwds  = self.pwd_edit.text()
            url   = self.url_edit.text()
            threads = self.thread_spin.value()
            use_tor = self.tor_check.isChecked()

            # Override the logger inside BruteForcer
            bf = BruteForcer(url, users, pwds, max_threads=threads, use_tor=use_tor)
            total = len(bf.usernames) * len(bf.passwords)
            done = 0

            # Monkey-patch save_hit & log_event to emit to GUI
            from utils.logger import save_hit, log_event
            def gui_save_hit(u, p):
                self.logger.log.emit(f"[+] HIT {u}:{p}")
            def gui_log_event(category, data):
                nonlocal done
                done += 1
                self.logger.progress.emit(done, total)
                if data.get("result") == "fail":
                    self.logger.log.emit(f"[-] {data['user']}:{data['password']}")
            setattr(bf, "save_hit", gui_save_hit)
            setattr(bf, "log_event", gui_log_event)

            bf.run()
            self.logger.log.emit("=== Finished ===")
            self._on_stop()  # re-enable start

        self.worker = threading.Thread(target=target, daemon=True)
        self.worker.start()

    def _on_stop(self):
        # No graceful kill in this simple example; recommend building a flag in BruteForcer
        self.start_btn.setEnabled(True)
        self.stop_btn .setEnabled(False)

    def _append_log(self, text):
        self.log_area.append(text)

    def _update_progress(self, done, total):
        self.progress.setMaximum(total)
        self.progress.setValue(done)
