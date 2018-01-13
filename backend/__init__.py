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
            response = self.factory.data_callback_fn(line)
            # As soon as any data is received, write it back.
            self.transport.write(response)


class MyServerFactory(ServerFactory):
    protocol = Echo

    def __init__(self, data_callback_fn):
        self.clients = []
        self.data_callback_fn = data_callback_fn


class SSLServer:
    def __init__(self, callback_fn: object, use_keyring, port: int = 8000) -> None:
        """
        Opens an echo socket server.
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

    def __init__(self, USE_KEYRING):
        QThread.__init__(self)
        self.USE_KEYRING = USE_KEYRING

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
        SSLServer(plugin_manager.handle_message, self.USE_KEYRING)

    def stopreactor(self):
        print("stopping")
        reactor.callFromThread(reactor.stop)
        print("stopping")
