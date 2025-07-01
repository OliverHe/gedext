from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

import globals

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(500, 500)
        self.setWindowTitle("About Gedext")

        qbtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        message = QLabel(globals.version)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self):
        print("That works")