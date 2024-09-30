import sys
from PySide6 import QtWidgets
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt,  QSignalMapper)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QFileDialog)



from main_window_ui2 import Ui_Fog

from fastfog import fog, wind

class MainWindow(QtWidgets.QMainWindow, Ui_Fog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    # Connect button signals to slots
        self.EncryptSizeField.setText("<Run the program to get the size>")
        self.EncryptInputFolderButton.clicked.connect(lambda: self.select_folder("Encrypt Input Folder", self.EncryptInputFolderLabel))
        self.EncryptOutputFolderButton.clicked.connect(lambda: self.select_folder("Encrypt Output Folder", self.EncryptOutputFolderLabel))
        self.DecryptInputFolderButton.clicked.connect(lambda: self.select_folder("Decrypt Input Folder", self.DecryptInputFolderLabel))
        self.DecryptOutputFolderButton.clicked.connect(lambda: self.select_folder("Decrypt Output Folder", self.DecryptOutputFolderLabel))
        self.ZipFileToEncryptButton.clicked.connect(lambda: self.select_file("Zip File To Encrypt", self.ZipFileToEncryptLabel))
        self.EncryptButton.clicked.connect(lambda: self.encrypt(self.EncryptKeyField.text(), self.ZipFileToEncryptLabel.toPlainText(), self.EncryptInputFolderLabel.toPlainText(), self.EncryptOutputFolderLabel.toPlainText()))
        self.DecryptButton.clicked.connect(lambda: self.decrypt(self.DecryptKeyField.text(), self.DecryptSizeField.text(), self.DecryptInputFolderLabel.toPlainText(), self.DecryptOutputFolderLabel.toPlainText()))

    def select_folder(self, title, labelname):
        folder_path = QFileDialog.getExistingDirectory(self, title)
        if folder_path:
            labelname.setText(folder_path)

    def select_file(self, title, labelname):
        file_path, _ = QFileDialog.getOpenFileName(self, title)
        if file_path:
            labelname.setText(file_path)

    def encrypt(self, key, file, input, output):
        size = fog(key, file, input, output)
        self.EncryptSizeField.setText(size)

    def decrypt(self, key, size, input, output):
        wind(key, int(size), input, output)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()