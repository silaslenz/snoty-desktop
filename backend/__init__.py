import logging
import ssl

import keyring
from PySide.QtCore import QThread
from twisted.internet import ssl, reactor
from twisted.internet.protocol import ServerFactory, Protocol

import frontend
import notifier_plugin
from backend.ctx_factory import CtxFactory

logger = logging.getLogger(__name__)


class Echo(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        logger.debug("Currently %d open connections.\n" % len(self.factory.clients))
        logger.debug(self.factory.clients)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        logger.debug("Lost connection")

    def dataReceived(self, data):
        logger.debug("Received data")
        for line in data.split(b"\n"):
            response = self.factory.data_callback_fn(line, self)
            # As soon as any data is received, write it back.


class MyServerFactory(ServerFactory):
    protocol = Echo

    def __init__(self, data_callback_fn):
        self.clients = []
        self.data_callback_fn = data_callback_fn


def start_reactor(callback_fn: object, use_keyring, port: int = 8000) -> None:
    """
    Opens an echo socket server.
    :param use_keyring: Whether to load certificate and key from keyring or files.
    :param callback_fn: Function to call when message was received
    :param port: Port to use
    """
    logger.info("Starting server")
    factory = MyServerFactory(data_callback_fn=callback_fn)
    if use_keyring:
        key = keyring.get_password("snoty", "key")
        certificate = keyring.get_password("snoty", "cert")
        reactor.listenSSL(port, factory, CtxFactory(key, certificate))
    else:
        reactor.listenSSL(port, factory,
                          ssl.DefaultOpenSSLContextFactory(
                              'key.pem', 'cert.pem'))
    reactor.run(installSignalHandlers=False)
    print("stopped")


class ServerThread(QThread):
    def __init__(self, use__keyring):
        """
        Sets up and runs the twisted ssl socket server.
        :param use__keyring:
        """
        QThread.__init__(self)
        self.use__keyring = use__keyring

    def __del__(self):
        self.wait()

    def run(self):
        logger.info("Starting plugin manager")
        # Register a plugin to manage incoming messages
        plugin_manager = frontend.PluginManager()
        # Show notifications as desktop notificationsL
        plugin_manager.register_plugin("Linux notifications", ["NotificationPosted"],
                                       [
                                           notifier_plugin.create_notification])
        logger.info("Starting server")
        start_reactor(plugin_manager.handle_message, self.use__keyring)

    @staticmethod
    def stop_reactor():
        """
        Stops the reactor from running so the thread can stop.
        """
        reactor.callFromThread(reactor.stop)
