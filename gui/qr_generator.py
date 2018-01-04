import qrcode
import zlib


def create_qr(ip, cert, compression_enabled=True):
    if compression_enabled:
        img = qrcode.make(zlib.compress(f"ip: {ip} cert: {cert}".encode()), box_size=6)
    else:
        img = qrcode.make(f"ip: {ip} cert: {cert}", box_size=5)
    img.show()


if __name__ == "__main__":
    with open("cert.pem") as file:
        create_qr("hej", file.read())
