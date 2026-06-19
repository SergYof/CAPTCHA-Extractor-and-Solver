from socket import socket
from struct import pack, unpack
from threading import Lock


class FramedSocket:
    _sock: socket
    _send_lock: Lock    # avoid simultaneous sending of information through a socket
    _receive_lock: Lock # avoid threaded receiving since it can break the protocol


    def __init__(self, sock: socket):
        self._sock = sock # IP address family, TCP connection
        self._send_lock = Lock()
        self._receive_lock = Lock()


    def _recv_exact(self, size: int) -> bytes:
        data = bytearray()

        while len(data) < size:
            chunk = self._sock.recv(size - len(data))

            if not chunk:
                raise ConnectionError("Socket closed while receiving data")

            data.extend(chunk)

        return bytes(data)


    def send(self, data: bytes) -> None:
        packet = pack("!I", len(data)) + data

        with self._send_lock:
            self._sock.sendall(packet)


    def receive(self) -> bytes:
        with self._receive_lock:
            data_len = unpack("!I", self._recv_exact(4))[0]
            data = self._recv_exact(data_len)

        return data
    

    def close(self):
        self._sock.close()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc, tb):
        self.close()