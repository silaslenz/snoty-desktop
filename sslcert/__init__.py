from genericpath import exists
import secrets
import keyring
import logging
from OpenSSL import crypto

logger = logging.getLogger(__name__)


def create_self_signed_cert() -> (bytes, bytes, str):
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


class SecretManager:
    def __init__(self, use_keyring):
        self.use_keyring = use_keyring

    def save_cert(self, cert):
        if self.use_keyring:
            keyring.set_password("snoty", "cert", cert)
        else:
            with open("cert.pem", "wb") as cert_file:
                cert_file.write(cert)

    def save_key(self, key):
        if self.use_keyring:
            keyring.set_password("snoty", "key", key)
        else:
            with open("key.pem", "wb") as key_file:
                key_file.write(key)

    def save_fingerprint(self, fingerprint):
        if self.use_keyring:
            keyring.set_password("snoty", "fingerprint", fingerprint)
        else:
            with open("fingerprint.pem", "wb") as key_file:
                key_file.write(fingerprint)

    def save_secret(self, secret):
        if self.use_keyring:
            keyring.set_password("snoty", "secret", secret)
        else:
            with open("secret.pem", "wb") as key_file:
                key_file.write(secrets.token_hex(16).encode())

    def get_fingerprint(self):
        if self.use_keyring:
            return keyring.get_password("snoty", "fingerprint")
        else:
            with open("fingerprint.pem", "rb") as key_file:
                return key_file.read().decode("ascii")

    def get_secret(self):
        if self.use_keyring:
            return keyring.get_password("snoty", "secret")
        else:
            with open("secret.pem", "rb") as key_file:
                return key_file.read().decode("ascii")

    def create_certificate_and_key(self) -> None:
        """
        Creates a self signed certificate, key and fingerprint, and then saves them.
        """
        logger.info("Cert and key NOT found, now generating")
        cert, key, fingerprint = create_self_signed_cert()

        self.save_cert(cert)
        self.save_key(key)
        self.save_fingerprint(fingerprint)
        self.save_secret(secrets.token_hex(16))
        logger.info("Cert and key saved")

    def certificate_and_key_exist(self) -> bool:
        """
        Checks if certificate, key and fingerprint exists.
        :return: If certificate, key and fingerprint exist.
        """
        if self.use_keyring:
            if keyring.get_password("snoty", "key") and keyring.get_password("snoty", "cert") and keyring.get_password(
                    "snoty", "fingerprint") and keyring.get_password("snoty", "secret"):
                logger.info("Cert and key found in keyring")
                return True
            else:
                return False
        else:
            if not exists("cert.pem") or not exists("key.pem") or not exists("fingerprint.pem") or not exists(
                    "secret.pem"):
                return False
            else:
                logger.info("Cert and key found in files")
                return True
