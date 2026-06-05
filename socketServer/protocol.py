from socket import socket
from struct import pack, unpack
from threading import Lock

PORT = 1234


class MessageSocket:
    _sock: socket
    _send_lock: Lock    # avoid simultaneous sending of information through a socket
    _receive_lock: Lock # avoid threaded receiving since it can break the protocol
    TEXT_LEN_SIZE = 1
    PAYLOAD_LEN_SIZE = 4


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


    def send(self, text: str, payload: bytes) -> None:
        text_bytes = text.encode("utf-8")

        if len(text_bytes) > 255:
            raise ValueError(
                "Text must be at most 255 bytes"
            )

        packet = (
            pack("!B", len(text_bytes))
            + text_bytes
            + pack("!I", len(payload))
            + payload
        )


        with self._send_lock:
            self._sock.sendall(packet)


    def receive(self) -> tuple[str, bytes]:
        with self._receive_lock:
            text_len = int.from_bytes(
                self._recv_exact(self.TEXT_LEN_SIZE),
                signed=False
            )

            text = self._recv_exact(text_len).decode("utf-8")


            payload_len = int.from_bytes(
                self._recv_exact(self.PAYLOAD_LEN_SIZE),
                byteorder="big",
                signed=False
            )

            payload = self._recv_exact(payload_len)


        return text, payload
    

    def close(self):
        self._sock.close()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc, tb):
        self.close()