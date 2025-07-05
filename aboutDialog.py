from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR

import globals

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 300)
        self.setWindowTitle("About Gedext")

        qbtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)

        gversion = QHBoxLayout()
        gversion.addWidget(QLabel('Gedext version:'))
        gversion.addWidget(QLabel(globals.version))

        qtver = QHBoxLayout()
        qtver.addWidget(QLabel('Qt version:'))
        qtver.addWidget(QLabel(QT_VERSION_STR))

        pqtver = QHBoxLayout()
        pqtver.addWidget(QLabel('PyQt version:'))
        pqtver.addWidget(QLabel(PYQT_VERSION_STR))

        layout = QVBoxLayout()
        layout.addLayout(gversion)
        layout.addLayout(qtver)
        layout.addLayout(pqtver)
        url = QLabel('<a href="https://github.com/OliverHe/gedext">Github</a>')
        url.setOpenExternalLinks(True)
        url.linkActivated.connect(self.url_clicked)
        layout.addWidget(url)
        cr = QLabel('Copyright Oliver Heesakkers, 2025')
        cr.setWordWrap(True)
        layout.addWidget(cr)
        lic = QLabel('License: GNU General Public License (GPL) v3')
        lic.setWordWrap(True)
        layout.addWidget(lic)
        layout.addStretch(100)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self):
        self.done(0)

    def url_clicked(self):
        print('Try and open the site')