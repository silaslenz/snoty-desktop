from OpenSSL import SSL, crypto
from twisted.internet import ssl


# Custom Contextfactory, identical to DefaultOpenSSLContextFactory,
# except for the fact that it takes the key/cert as string instead of filenames


class CtxFactory(ssl.ContextFactory):
    """
        L{DefaultOpenSSLContextFactory} is a factory for server-side SSL context
        objects.  These objects define certain parameters related to SSL
        handshakes and the subsequent connection.

        @ivar _contextFactory: A callable which will be used to create new
            context objects.  This is typically L{OpenSSL.SSL.Context}.
        """
    _context = None

    def __init__(self, private_key: str, certificate: str,
                 sslmethod=SSL.SSLv23_METHOD, _contextFactory=SSL.Context):
        """
        @param private_key: private key
        @param certificate: certificate
        @param sslmethod: The SSL method to use
        """
        self.private_key = private_key
        self.certificate = certificate
        self.sslmethod = sslmethod
        self._contextFactory = _contextFactory

        # Create a context object right now.  This is to force validation of
        # the given parameters so that errors are detected earlier rather
        # than later.
        self.cacheContext()

    def cacheContext(self):
        if self._context is None:
            ctx = self._contextFactory(self.sslmethod)
            # Disallow SSLv2!  It's insecure!  SSLv3 has been around since
            # 1996.  It's time to move on.
            ctx.set_options(SSL.OP_NO_SSLv2)
            ctx.use_certificate(crypto.load_certificate(crypto.FILETYPE_PEM, self.certificate))
            ctx.use_privatekey(crypto.load_privatekey(crypto.FILETYPE_PEM, self.private_key))
            self._context = ctx

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['_context']
        return d

    def __setstate__(self, state):
        self.__dict__ = state

    def getContext(self):
        """
        Return an SSL context.
        """
        return self._context
