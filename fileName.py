import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class fileName(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('CSV Name')
        # self.setWindowIcon(QIcon("Deliverables/pdf_icon.png"))
        self.setFixedSize(350, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()

        self.label = QLabel('<b>Enter file name:</b>')
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        self.button = QPushButton('Save', self)
        self.button.clicked.connect(lambda: self.on_save())
        layout.addWidget(self.button)

        self.setLayout(layout)

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screenGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_save(self):
        self.file_name = self.textbox.text()
        if not self.file_name.endswith('.csv'):
            self.file_name += '.csv'
        self.accept()
