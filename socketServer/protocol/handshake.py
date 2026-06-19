from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from .framing import FramedSocket


def server_rsa_handshake(sock: FramedSocket, public_key: RSA.RsaKey, private_key: RSA.RsaKey) -> bytes:
    sock.send(public_key.export_key("DER"))
    
    encrypted_key = sock.receive()

    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_key)
    sock.send(b"ACK")
    
    return aes_key


def client_rsa_handshake(sock: FramedSocket) -> bytes:
    aes_key = get_random_bytes(32)
    server_public_key = RSA.import_key(sock.receive())

    rsa_cipher = PKCS1_OAEP.new(server_public_key)
    encrypted_key = rsa_cipher.encrypt(aes_key)
    sock.send(encrypted_key)
    
    if sock.receive() != b"ACK":
        raise RuntimeError("Handshake failed!")
    
    return aes_key
