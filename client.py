import socket, ssl, pprint, json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="cert.pem",
                           cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect(('localhost', 8000))

print (repr(ssl_sock.getpeername()))
print (ssl_sock.cipher())
print (pprint.pformat(ssl_sock.getpeercert()))

ssl_sock.write(json.dumps({"type": "notification", "data" : "hey"}).encode())

print(f"Response: {ssl_sock.read()}")