import logging
import sys

import keyring
from PyQt5.QtWidgets import QApplication

import backend
from gui.Window import MainWindow
from sslcert import SecretManager

USE_KEYRING = False

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info(f"Using keyring for storage: {USE_KEYRING}")


def get_local_ip() -> str:
    """
    Get local IP. Requires internet access to work.
    :return: Local ip
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    logger.info(f"Local IP is {ip}")
    return ip


if __name__ == "__main__":
    secret_manager = SecretManager(USE_KEYRING)
    # Make sure key and certificate exist, and if not, create them.
    if not secret_manager.certificate_and_key_exist():
        secret_manager.create_certificate_and_key()

    app = QApplication(sys.argv)

    myThread = backend.ServerThread(USE_KEYRING, secret_manager)
    myThread.start()

    mainWin = MainWindow(get_local_ip(), secret_manager.get_fingerprint(),
                         secret_manager.get_secret(), myThread)
    mainWin.show()
    sys.exit(app.exec_())
