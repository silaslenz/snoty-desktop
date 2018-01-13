import logging
import sys
from os.path import exists

import keyring
from PyQt5.QtWidgets import QApplication

import backend
import sslcert
from gui.Window import MainWindow

USE_KEYRING = True

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info(f"Using keyring for storage: {USE_KEYRING}")


def certificate_and_key_exist():
    if USE_KEYRING:
        if keyring.get_password("snoty", "key") and keyring.get_password("snoty", "cert") and keyring.get_password(
                "snoty", "fingerprint"):
            logger.info("Cert and key found in keyring")
            return True
        else:
            return False
    else:
        if not exists("cert.pem") or not exists("key.pem") or not exists("fingerprint.pem"):
            return False
        else:
            logger.info("Cert and key found in files")
            return True


def create_certificate_and_key():
    logger.info("Cert and key NOT found, now generating")
    cert, key, fingerprint = sslcert.create_self_signed_cert()
    if USE_KEYRING:
        sslcert.save_cert_in_keyring(cert)
        sslcert.save_key_in_keyring(key)
        sslcert.save_fingerprint_in_keyring(fingerprint)
        logger.info("Cert and key saved in keyring")
    else:
        with open("cert.pem", "wb") as cert_file:
            cert_file.write(cert)
        with open("key.pem", "wb") as key_file:
            key_file.write(key)
        with open("fingerprint.pem", "wb") as key_file:
            key_file.write(fingerprint)
        logger.info("Cert and key saved in files")


def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # Make sure key and certificate exist, and if not, create them.
    if not certificate_and_key_exist():
        create_certificate_and_key()

    app = QApplication(sys.argv)
    myThread = backend.ServerThread(USE_KEYRING)
    myThread.start()
    mainWin = MainWindow(get_local_ip(), keyring.get_password("snoty", "fingerprint"), myThread)
    mainWin.show()
    sys.exit(app.exec_())
