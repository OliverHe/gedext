#from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QFont, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, \
    QPlainTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel
from time import localtime, strftime

import globals

from base64 import b64decode
import json
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import xml.dom.minidom

from aboutDialog import AboutDialog

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

        pagelayout.addLayout(button_layout)
        pagelayout.addWidget(self.txt)

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

        button_layout.addWidget(QLabel())

        btn = QPushButton("Clear")
        btn.pressed.connect(self.btn_clear_clicked)
        button_layout.addWidget(btn)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")
        help_menu = menu.addMenu("&Help")

        actn_about = QAction("&About", self)
        actn_about.triggered.connect(self.actn_about_clicked)
        help_menu.addAction(actn_about)

        actn_quit = QAction("&Quit", self)
        actn_quit.triggered.connect(self.actn_quit_clicked)
        file_menu.addAction(actn_quit)

        actn_tstamp = QAction("Insert &timestamp", self)
        actn_tstamp.triggered.connect(self.actn_tstamp_clicked)
        actn_tstamp.setShortcut(QKeySequence("Alt+Shift+t"))
        edit_menu.addAction(actn_tstamp)

        actn_nwlines = QAction("Convert &newlines", self)
        actn_nwlines.triggered.connect(self.actn_nwlines_clicked)
        actn_nwlines.setShortcut(QKeySequence("Alt+Shift+n"))
        edit_menu.addAction(actn_nwlines)

        widget = QWidget()
        widget.setLayout(pagelayout)

        self.stbar = QStatusBar()
        self.stbar.showMessage("Insert text and press one of the buttons")
        self.stbar.addPermanentWidget(QLabel(globals.version))

        self.setCentralWidget(widget)
        self.setStatusBar(self.stbar)

    def actn_nwlines_clicked(self):
        txtstr = self.hpr_find_txtstr()
        outp = txtstr.replace('\\n', '\n')
        self.hpr_strep(outp)

    def actn_tstamp_clicked(self):
        tstamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.txt.appendPlainText(str(tstamp) + ': ')

    def actn_quit_clicked(self):
        app.quit()

    def actn_about_clicked(self):
        dlg = AboutDialog()
        dlg.exec()

    def hpr_find_txtstr(self):
        # Get the text to be processed
        cursor = self.txt.textCursor()
        if cursor.hasSelection():
            txtstr = cursor.selectedText()
        else:
            txtstr = self.txt.toPlainText()
        return txtstr

    def hpr_strep(self, o):
        cursor = self.txt.textCursor()
        if cursor.hasSelection():
            cursor.deleteChar()
            cursor.insertText(o)
        else:
            self.txt.setPlainText(o)

    def btn_clear_clicked(self):
        self.txt.setPlainText('')
        self.stbar.showMessage('Cleared all text')

    def btn_b64_clicked(self):
        # Get the text to be processed
        txtstr = self.hpr_find_txtstr()

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

        # Replace text buffer with result
        if res:
            self.hpr_strep(res)

    def btn_json_clicked(self):
        # Get the text to be processed
        txtstr = self.hpr_find_txtstr()

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
            self.hpr_strep(outp)

    def x509_obj2str(self, o):
        res = ''
        for attr in o:
            res = res + ', ' + attr.oid._name + ': ' + attr.value
        return res[2:]

    def btn_x509_clicked(self):
        # Get the text to be processed
        txtstr = self.hpr_find_txtstr()

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
            for attr in cert.extensions:
                if attr.oid._name in ['subjectAltName']:
                    outp = outp + '\nSAN: '
                    for item in attr.value._general_names:
                        outp = outp + item.value + "\n     "

                if attr.oid._name in ['keyUsage',
                                       'basicConstraints',
                                       'subjectKeyIdentifier',
                                       'authorityKeyIdentifier']:
                    outp = outp + str(attr.value) + "\n"

            # Handover to helper function replacing the text in the window
            self.hpr_strep(outp)

    def btn_xml_clicked(self):
        # Get the text to be processed
        txtstr = self.hpr_find_txtstr()

        # If there is nothing to process, return early
        if not txtstr:
            self.stbar.showMessage("Need more input")
            return
        try:
            dom = xml.dom.minidom.parseString(txtstr)
            xmlo = dom.toprettyxml()
            msg = f"XML decode OK"
        except Exception as err:
            xmlo = None
            msg = f"XML decode FAIL: {err}"

        if xmlo:
            self.hpr_strep(xmlo)

        self.stbar.showMessage(msg)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
