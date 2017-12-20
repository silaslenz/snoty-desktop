import threading
import socket
import ssl


class SSLServer:
    def __init__(self, callback_fn, port=10023):
        self.callback_fn = callback_fn
        self.port = port

        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False

        thread.start()

    def get_socket(self):
        bindsocket = socket.socket()
        bindsocket.bind(('', self.port))
        bindsocket.listen()
        return bindsocket

    def deal_with_client(self, connstream):
        data = connstream.read()
        while data:
            self.callback_fn(data)
            data = connstream.read()

    def run(self):
        bindsocket = self.get_socket()
        newsocket, fromaddr = bindsocket.accept()
        while True:
            connstream = self.context.wrap_socket(newsocket, server_side=True)
            try:
                self.deal_with_client(connstream)
            finally:
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()

