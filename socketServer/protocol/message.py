from enum import IntEnum
from typing import Any
from struct import pack, unpack


class MessageType(IntEnum):
    TEXT = 1
    BINARY = 2


class Message:
    type: MessageType
    payload: Any    # variable type, depends on message type


    def __init__(self, type, payload):
        self.type = type
        self.payload = payload


    def encode(self) -> bytes:
        encoded_payload: bytes
        match self.type:
            case MessageType.TEXT:
                assert type(self.payload) == str
                encoded_payload = self.payload.encode()
            case MessageType.BINARY:
                assert type(self.payload) == bytes
                encoded_payload = self.payload
            case _:
                raise ValueError(f"Invalid message type: {self.type}")

        return pack("!BI", self.type, len(encoded_payload)) + encoded_payload
    

    @staticmethod
    def decode(frame: bytes):
        # decode a frame and return the message
        type, length = unpack("!BI", frame[:5])
        match type:
            case MessageType.TEXT:
                payload = frame[5:5 + length].decode()
            case MessageType.BINARY:
                payload = frame[5:5 + length]
            case _:
                raise ValueError(f"Invalid message type {type}")
        
        return Message(type, payload)