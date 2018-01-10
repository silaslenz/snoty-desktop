import keyring
import logging
from OpenSSL import crypto

logger = logging.getLogger(__name__)


def create_self_signed_cert() -> (bytes, bytes):
    """
    Generate a certificate key pair.
    :return: certificate, key, fingerprint
    """
    # create a key pair)
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "AT"
    cert.get_subject().ST = "Styria"
    cert.get_subject().L = "Graz"
    # Valid for a year
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    logger.info(f"Creating cert with the following information: {cert.get_subject()}")
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    cert_dump = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    key_dump = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
    return cert_dump, key_dump, cert.digest("sha256")


def save_cert_in_keyring(cert):
    keyring.set_password("snoty", "cert", cert)


def save_key_in_keyring(key):
    keyring.set_password("snoty", "key", key)


def save_fingerprint_in_keyring(fingerprint):
    keyring.set_password("snoty", "fingerprint", fingerprint)


def get_cert_from_keyring():
    keyring.get_password("snoty", "cert")


def get_key_from_keyring():
    keyring.get_password("snoty", "key")


if __name__ == "__main__":
    cert, key, fingerprint = create_self_signed_cert()
    print(fingerprint)
    # save_cert_in_keyring(cert)
    # save_key_in_keyring(key)
