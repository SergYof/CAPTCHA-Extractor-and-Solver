from socket import socket, AF_INET, SOCK_STREAM
from .protocol import SecureConnection, PORT


def create_client_conn() -> SecureConnection:
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect(("127.0.0.1", PORT))
    return SecureConnection(client_sock, False)