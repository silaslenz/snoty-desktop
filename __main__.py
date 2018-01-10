import logging
import sys
from os.path import exists

import keyring
from PySide.QtCore import QThread
from PySide.QtGui import QApplication

import backend
import frontend
import notifier_plugin
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


class ServerThread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        logger.info("Starting plugin manager")
        # Register a plugin to manage incoming messages
        plugin_manager = frontend.PluginManager()
        # plugin_manager.register_plugin("printer", ["notification"],[print_stuff])  # Print notifications to console
        plugin_manager.register_plugin("Linux notifications", ["NotificationPosted"],
                                       [
                                           notifier_plugin.create_notification])  # Show notifications as desktop notifications
        logger.info("Starting server")
        backend.SSLServer(plugin_manager.handle_message, USE_KEYRING)


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
    mainWin = MainWindow(get_local_ip(), keyring.get_password("snoty", "fingerprint"), ServerThread)
    mainWin.show()
    sys.exit(app.exec_())
