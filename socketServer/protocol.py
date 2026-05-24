from socket import socket

PORT = 1234


class MessageSocket:
    sock: socket
    length_size: int


    def __init__(self, sock: socket, *, length_size: int = 4):
        self.sock = sock # IP address family, TCP connection
        self.length_size = length_size


    def _recv_exact(self, size: int) -> bytes:
        data = bytearray()

        while len(data) < size:
            chunk = self.sock.recv(size - len(data))

            if not chunk:
                raise ConnectionError("Socket closed while receiving data")

            data.extend(chunk)

        return bytes(data)


    def send(self, data: bytes) -> None:
        length_prefix = len(data).to_bytes(
            length=self.length_size,
            byteorder="big",
            signed=False
        )
        self.sock.sendall(length_prefix + data)


    def receive(self) -> bytes:
        length_data = self._recv_exact(self.length_size)
        message_length = int.from_bytes(length_data)

        return self._recv_exact(message_length)
    

    def close(self):
        self.sock.close()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc, tb):
        self.close()