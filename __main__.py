import logging
import sys

import keyring
from PyQt5.QtWidgets import QApplication

import backend
from gui.Window import MainWindow
from sslcert import create_certificate_and_key, certificate_and_key_exist

USE_KEYRING = True

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
    # Make sure key and certificate exist, and if not, create them.
    if not certificate_and_key_exist(USE_KEYRING):
        create_certificate_and_key(USE_KEYRING)

    app = QApplication(sys.argv)

    myThread = backend.ServerThread(USE_KEYRING)
    myThread.start()

    mainWin = MainWindow(get_local_ip(), keyring.get_password("snoty", "fingerprint"),
                         keyring.get_password("snoty", "secret"), myThread)
    mainWin.show()
    sys.exit(app.exec_())
