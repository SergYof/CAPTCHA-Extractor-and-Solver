from socket import socket, AF_INET, SOCK_STREAM
from protocol import MessageSocket, PORT


def create_client_ms() -> MessageSocket:
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect(("127.0.0.1", PORT))
    return MessageSocket(client_sock)