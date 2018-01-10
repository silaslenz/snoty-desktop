import qrcode
import sys
import PySide
sys.modules['PyQt5'] = PySide
from PySide import QtCore
from PySide.QtCore import QSize
from PySide.QtGui import QMainWindow, QWidget, QGridLayout, QLabel, QPixmap


from PIL.ImageQt import ImageQt



class MainWindow(QMainWindow):
    def __init__(self, ip, fingerprint, ServerThread):
        QMainWindow.__init__(self)

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
        self.myThread = ServerThread()
        self.myThread.start()
