import pprint
import socket
import ssl

from sslcert import SecretManager

secret_manager = SecretManager(False)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="cert.pem")
#                           cert_reqs=ssl.CERT_REQUIRED) # Ignore for now, requires file
ssl_sock.connect(('localhost', 9096))

print(repr(ssl_sock.getpeername()))
print(ssl_sock.cipher())
print(pprint.pformat(ssl_sock.getpeercert()))
print(type(secret_manager.get_secret().encode()))
data = '{"secret" : "' + secret_manager.get_secret() + '", "type": "NotificationPosted", "id": "com.textra#4", "package": "com.textra", "isUpdate": true, "title": "Big Text", "text": "Notification Sub Text", "actions": [{"id": 0, "label": "Als ungelesen markieren", "input": false}, {"id": 1, "label": "Antworten", "input": true}], "clearable": true}\n'
ssl_sock.write(
    data.encode())

ssl_sock.settimeout(10)
print(f"Response: {ssl_sock.recv(4096)}")
