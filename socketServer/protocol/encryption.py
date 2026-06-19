from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AESCipher:
    _key: bytes
    NONCE_SIZE = 12
    TAG_SIZE = 16


    def __init__(self, key: bytes):
        self._key = key


    def encrypt(self, data: bytes) -> bytes:
        nonce = get_random_bytes(self.NONCE_SIZE)
        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return bytes(cipher.nonce) + tag + ciphertext


    def decrypt(self, data: bytes) -> bytes:
        nonce = data[:self.NONCE_SIZE]

        tag = data[
            self.NONCE_SIZE:
            self.NONCE_SIZE + self.TAG_SIZE
        ]

        ciphertext = data[self.NONCE_SIZE + self.TAG_SIZE:]
        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)

        return cipher.decrypt_and_verify(ciphertext, tag)
