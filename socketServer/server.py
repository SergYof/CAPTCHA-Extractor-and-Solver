from socket import socket, AF_INET, SOCK_STREAM
from protocol import MessageSocket, PORT


def create_listening_socket() -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("127.0.0.1", PORT))
    sock.listen(1)
    return sock


def accept_client_ms(server_sock: socket) -> MessageSocket:
    client_sock, _ = server_sock.accept()
    return MessageSocket(client_sock)


def main():
    server_sock = create_listening_socket()
    client_ms = accept_client_ms(server_sock)
    
    data = client_ms.receive()

    print(data.hex())

    # TODO: do something with the data received


if __name__ == "__main__":
    main()