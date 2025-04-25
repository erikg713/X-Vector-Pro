from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QTextEdit
from core.settings import (
    load_settings,
    save_settings,
    toggle_stealth_mode,
    get_settings_summary
)

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_current_settings()

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

    def load_current_settings(self):
        try:
            config = load_settings()
            self.stealth_checkbox.setChecked(config.get("stealth_mode", False))
            self.output.setText(get_settings_summary(config))
        except Exception as e:
            self.output.setText(f"Failed to load settings: {str(e)}")

    def handle_save(self):
        stealth = self.stealth_checkbox.isChecked()
        try:
            toggle_stealth_mode(stealth)
            config = {"stealth_mode": stealth}
            save_settings(config)
            self.output.setText(get_settings_summary(config))
        except Exception as e:
            self.output.setText(f"Error saving settings: {str(e)}")
