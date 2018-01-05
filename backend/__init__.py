import logging
import ssl

from twisted.internet import ssl, reactor
from twisted.internet.protocol import ServerFactory, Protocol

logger = logging.getLogger(__name__)


class Echo(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        logger.debug("Currently %d open connections.\n" % len(self.factory.clients))

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        logger.debug("Lost connection")

    def dataReceived(self, data):
        logger.debug("Received data")
        response = self.factory.data_callback_fn(data)
        # As soon as any data is received, write it back.
        self.transport.write(response)


class MyServerFactory(ServerFactory):
    protocol = Echo

    def __init__(self, data_callback_fn):
        self.clients = []
        self.data_callback_fn = data_callback_fn


class SSLServer:
    def __init__(self, callback_fn: object, port: int = 8000) -> None:
        """
        Opens an echo socket server.
        :param callback_fn: Function to call when message was received
        :param port: Port to use
        """
        logger.info("Starting server")
        factory = MyServerFactory(data_callback_fn=callback_fn)
        reactor.listenSSL(port, factory,
                          ssl.DefaultOpenSSLContextFactory(
                              'key.pem', 'cert.pem'))
        reactor.run()
