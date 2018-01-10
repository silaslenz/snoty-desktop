import logging
import keyring
from os.path import exists

import backend
import frontend
import sslcert
import notifier_plugin

USE_KEYRING = True

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info(f"Using keyring for storage: {USE_KEYRING}")


def print_stuff(stuff):
    print(stuff)
    return f"I got {stuff}".encode()


def certificate_and_key_exist():
    if USE_KEYRING:
        if keyring.get_password("snoty", "key") and keyring.get_password("snoty", "cert"):
            logger.info("Cert and key found in keyring")
            return True
        else:
            return False
    else:
        if not exists("cert.pem") or not exists("key.pem"):
            return False
        else:
            logger.info("Cert and key found in files")
            return True


if __name__ == "__main__":
    # Make sure key and certificate exist, and if not, create them.
    if not certificate_and_key_exist():
        logger.info("Cert and key NOT found, now generating")
        cert, key = sslcert.create_self_signed_cert()
        if USE_KEYRING:
            sslcert.save_cert_in_keyring(cert)
            sslcert.save_key_in_keyring(key)
            logger.info("Cert and key saved in keyring")
        else:
            with open("cert.pem", "wb") as cert_file:
                cert_file.write(cert)
            with open("key.pem", "wb") as key_file:
                key_file.write(key)
            logger.info("Cert and key saved in files")

    logger.info("Starting plugin manager")
    # Register a plugin to manage incoming messages
    plugin_manager = frontend.PluginManager()
    # plugin_manager.register_plugin("printer", ["notification"],[print_stuff])  # Print notifications to console
    plugin_manager.register_plugin("Linux notifications", ["NotificationPosted"],
                                   [notifier_plugin.create_notification])  # Show notifications as desktop notifications
    logger.info("Starting server")
    server = backend.SSLServer(plugin_manager.handle_message, USE_KEYRING)
