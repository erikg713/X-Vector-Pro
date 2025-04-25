from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QTextEdit
from core.settings import toggle_stealth_mode, get_settings_summary  # expected core functions
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton, QTextEdit
from core.settings import load_settings, save_settings, get_settings_summary

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.stealth_checkbox = QCheckBox("Enable Stealth Mode")
        self.save_button = QPushButton("Save Settings")
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)

        layout.addWidget(self.stealth_checkbox)
        layout.addWidget(self.save_button)
        layout.addWidget(self.summary_output)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.handle_save)
        self.load_current_settings()

    def load_current_settings(self):
        config = load_settings()
        self.stealth_checkbox.setChecked(config.get("stealth_mode", False))
        self.summary_output.setText(get_settings_summary(config))

    def handle_save(self):
        config = {
            "stealth_mode": self.stealth_checkbox.isChecked()
        }
        save_settings(config)
        self.summary_output.setText(get_settings_summary(config))
class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.stealth_checkbox = QCheckBox("Enable Stealth Mode")
        self.save_button = QPushButton("Save Settings")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.stealth_checkbox)
        layout.addWidget(self.save_button)
        layout.addWidget(self.output)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.handle_save)

    def handle_save(self):
        stealth = self.stealth_checkbox.isChecked()
        try:
            toggle_stealth_mode(stealth)
            self.output.setText(get_settings_summary())
        except Exception as e:
            self.output.setText(f"Error: {str(e)}")
