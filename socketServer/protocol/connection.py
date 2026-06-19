from socket import socket
from Crypto.PublicKey import RSA
from .encryption import AESCipher
from .handshake import client_rsa_handshake, server_rsa_handshake
from .framing import FramedSocket
from .message import Message


class SecureConnection:
    _sock: FramedSocket
    _cipher: AESCipher


    def __init__(self, sock: socket, isServer: bool):
        self._sock = FramedSocket(sock)
        
        if isServer:
            private_key = RSA.generate(2048)
            public_key = private_key.public_key()
            aes_key = server_rsa_handshake(self._sock, public_key, private_key)
        else:
            aes_key = client_rsa_handshake(self._sock)
        
        self._cipher = AESCipher(aes_key)


    def send(self, msg: Message) -> None:
        raw_msg = msg.encode()
        encrypted_msg = self._cipher.encrypt(raw_msg)
        
        self._sock.send(encrypted_msg)

    
    def receive(self) -> Message:
        encrypted = self._sock.receive()
        raw = self._cipher.decrypt(encrypted)

        return Message.decode(raw)


    def close(self):
        self._sock.close()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc, tb):
        self.close()