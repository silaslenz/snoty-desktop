import qrcode
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self, ip, fingerprint, secret, server_thread):
        """
        Main window. Shows image with qr code generated from arguments
        :param ip: Local ip adress
        :param fingerprint: Fingerprint (sha256) of certificate
        :param server_thread: backend.ServerThread
        """
        QMainWindow.__init__(self)

        self.server_thread = server_thread
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Snoty")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)
        central_widget.setLayout(grid_layout)

        title = QLabel("Hello cats!", self)
        title.setAlignment(QtCore.Qt.AlignCenter)

        img = qrcode.make(f"{ip} {fingerprint} {secret}".encode(), box_size=6)
        image = ImageQt(img)
        pixmap = QPixmap.fromImage(image)
        title.setPixmap(pixmap)

        grid_layout.addWidget(title, 0, 0)

    def closeEvent(self, event):
        """
        Called when window closes. Asks twisted to shut down and continues closing when done.
        :param event:
        """
        self.server_thread.stop_reactor()
        self.server_thread.wait()
        event.accept()
