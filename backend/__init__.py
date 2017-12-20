import ssl

from twisted.internet import ssl, reactor
from twisted.internet.protocol import ServerFactory, Protocol


class Echo(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print("Currently %d open connections.\n" % len(self.factory.clients))

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Lost connection")

    def dataReceived(self, data):
        response = self.factory.data_callback_fn(data)
        """As soon as any data is received, write it back."""
        self.transport.write(response)


class MyServerFactory(ServerFactory):
    protocol = Echo

    def __init__(self, data_callback_fn):
        self.clients = []
        self.data_callback_fn = data_callback_fn


class SSLServer:
    def __init__(self, callback_fn, port=10023):
        factory = MyServerFactory(data_callback_fn=callback_fn)
        reactor.listenSSL(8000, factory,
                          ssl.DefaultOpenSSLContextFactory(
                              'key.pem', 'cert.pem'))
        reactor.run()
