import qrcode
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self, ip, fingerprint, myThread):
        QMainWindow.__init__(self)

        self.myThread = myThread
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Snoty")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        title = QLabel("Hello cats!", self)
        title.setAlignment(QtCore.Qt.AlignCenter)

        img = qrcode.make(f"{ip} {fingerprint}".encode(), box_size=6)
        image = ImageQt(img)
        pixmap = QPixmap.fromImage(image)
        title.setPixmap(pixmap)
        gridLayout.addWidget(title, 0, 0)

    def closeEvent(self, event):
        self.myThread.stopreactor()
        self.myThread.wait()
        event.accept()
