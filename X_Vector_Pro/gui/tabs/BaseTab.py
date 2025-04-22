from PyQt5.QtWidgets import QWidget

class BaseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        raise NotImplementedError("Must be implemented in subclass")
