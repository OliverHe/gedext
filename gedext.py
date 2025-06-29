from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPageLayout, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QToolBar, QPlainTextEdit, QVBoxLayout, \
    QHBoxLayout, QStackedLayout, QPushButton, QWidget

from base64 import b64decode
import json

from cryptography import x509
from cryptography.hazmat.backends import default_backend


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gedext")
        self.setMinimumSize(700,800)

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        font = QFont()
        font.setFamily("monospace")
        font.setPointSize(10)
        self.txt = QPlainTextEdit()
        self.txt.setFont(font)

        self.txtspace = QStackedLayout()
        self.txtspace.addWidget(self.txt)

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.txtspace)

        btn = QPushButton("B64 decode")
        btn.pressed.connect(self.btn_b64_clicked)
        button_layout.addWidget(btn)

        btn = QPushButton("X.509")
        btn.pressed.connect(self.btn_x509_clicked)
        button_layout.addWidget(btn)

        btn = QPushButton("JSON")
        btn.pressed.connect(self.btn_json_clicked)
        button_layout.addWidget(btn)

        btn = QPushButton("XML")
        btn.pressed.connect(self.btn_xml_clicked)
        button_layout.addWidget(btn)

        #toolbar = QToolBar("Ready")
        #self.addToolBar(toolbar)

        widget = QWidget()
        widget.setLayout(pagelayout)

        self.stbar = QStatusBar()
        self.stbar.showMessage("Insert text and press one of the buttons")

        self.setCentralWidget(widget)
        self.setStatusBar(self.stbar)

    def btn_b64_clicked(self):
        # Get all the text in the window
        txtstr = self.txt.toPlainText()

        # If there is nothing to save return early
        if not txtstr:
            self.stbar.showMessage("Need more input")
            return

        try:
            res = b64decode(txtstr).decode('UTF-8')
            msg = f"Base64 decode OK"
        except Exception as err:
            res = None
            msg = f"Base64 decode FAIL: {err}"

        self.stbar.showMessage(msg)

        #Replace text buffer with result
        if res:
            self.txt.setPlainText(res)

    def btn_json_clicked(self):
        # Get all the text in the window
        txtstr = self.txt.toPlainText()

        # If there is nothing to save return early
        if not txtstr:
            self.stbar.showMessage("Need more input")
            return

        try:
            res = json.loads(txtstr)
            msg = f"JSON decode OK"
        except Exception as err:
            res = None
            msg = f"JSON decode FAIL: {err}"

        self.stbar.showMessage(msg)

        if res:
            outp=json.dumps(res, sort_keys=True, indent=4)
            self.txt.setPlainText(outp)

    def x509_obj2str(self, o):
        res = ''
        for attrb in o:
            res = res + ', ' + attrb.oid._name + ': ' + attrb.value
        return res[2:]

    def btn_x509_clicked(self):
        # Get all the text in the window
        txtstr = self.txt.toPlainText()

        # If there is nothing to save return early
        if not txtstr:
            self.stbar.showMessage("Need more input")
            return

        # Convert to bytes
        txtb = bytes(txtstr, 'UTF-8')
        try:
            cert = x509.load_pem_x509_certificate(txtb, default_backend())
            msg = f"X509 decode OK"
        except Exception as err:
            cert = None
            msg = f"X509 decode FAIL: {err}"

        self.stbar.showMessage(msg)

        if cert:
            outp = 'Subject: ' + self.x509_obj2str(cert.subject) + "\n"
            outp = outp + 'Issuer : ' + self.x509_obj2str(cert.issuer) + "\n"
            outp = outp + f"Not valid before: {cert.not_valid_before_utc}\n"
            outp = outp + f"Not valid after : {cert.not_valid_after_utc}\n\n"
            # print('Extensions : ' + _obj2str(cert.extensions))
            for attrb in cert.extensions:
                if attrb.oid._name in ['subjectAltName']:
                    outp = outp + '\nSAN: '
                    for item in attrb.value._general_names:
                        outp = outp + item.value + "\n     "

                if attrb.oid._name in ['keyUsage', 'basicConstraints', 'subjectKeyIdentifier',
                                       'authorityKeyIdentifier']:
                    outp = outp + str(attrb.value) + "\n"

            self.txt.setPlainText(outp)

    def btn_xml_clicked(self):
        self.stbar.showMessage("Still working on that")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()