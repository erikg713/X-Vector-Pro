import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QComboBox
from PyQt5.QtCore import QFileSystemWatcher

LOG_DIR = "logs"

class HistoryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select a log file to view:")
        self.dropdown = QComboBox()
        self.viewer = QTextEdit()
        self.viewer.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

        self.refresh_log_list()

        self.dropdown.currentIndexChanged.connect(self.load_selected_log)

        # Optional: auto-refresh log list when files change
        self.watcher = QFileSystemWatcher([LOG_DIR])
        self.watcher.directoryChanged.connect(self.refresh_log_list)

    def refresh_log_list(self):
        self.dropdown.clear()
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        files = sorted(f for f in os.listdir(LOG_DIR) if f.endswith(".json"))
        self.dropdown.addItems(files)
        if files:
            self.load_selected_log(0)

    def load_selected_log(self, index):
        file_name = self.dropdown.currentText()
        if not file_name:
            return

        full_path = os.path.join(LOG_DIR, file_name)
        try:
            with open(full_path, "r") as f:
                contents = f.read()
            self.viewer.setText(contents)
        except Exception as e:
            self.viewer.setText(f"Error reading log: {str(e)}")
