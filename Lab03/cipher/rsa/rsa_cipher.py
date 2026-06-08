from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

KEY_DIR = 'cipher/rsa/keys'

if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)


class RSACipher:
    def __init__(self):
        pass

    def generate_keys(self):
        key = RSA.generate(2048)

        with open(f'{KEY_DIR}/privateKey.pem', 'wb') as f:
            f.write(key.export_key())

        with open(f'{KEY_DIR}/publicKey.pem', 'wb') as f:
            f.write(key.publickey().export_key())

    def load_keys(self):
        with open(f'{KEY_DIR}/privateKey.pem', 'rb') as f:
            private_key = RSA.import_key(f.read())

        with open(f'{KEY_DIR}/publicKey.pem', 'rb') as f:
            public_key = RSA.import_key(f.read())

        return private_key, public_key

    def encrypt(self, plain_text):
        _, public_key = self.load_keys()
        cipher = PKCS1_OAEP.new(public_key)
        encrypted = cipher.encrypt(plain_text.encode('utf-8'))
        return encrypted

    def decrypt(self, cipher_bytes):
        private_key, _ = self.load_keys()
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(cipher_bytes)
        return decrypted.decode('utf-8')

    def sign(self, message):
        private_key, _ = self.load_keys()
        h = SHA256.new(message.encode('utf-8'))
        signature = pkcs1_15.new(private_key).sign(h)
        return signature

    def verify(self, message, signature):
        _, public_key = self.load_keys()
        h = SHA256.new(message.encode('utf-8'))
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
