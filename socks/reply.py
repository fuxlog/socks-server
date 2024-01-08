from .utils import bytes_address
from .session import Session
from .cryption import generate_key, encrypt_data
import zlib


class Reply:
    def __init__(self, version: int, reply_status: int, reserved: int, address_type: int, bind_host: str, bind_port: int):
        self.version = version
        self.reply_status = reply_status
        self.reserved = reserved
        self.address_type = address_type
        self.bind_host = bind_host
        self.bind_port = bind_port

    def to_bytes(self) -> bytes:
        return self.version.to_bytes(1, "big") + self.reply_status.to_bytes(1, "big") \
                + self.reserved.to_bytes(1, "big") + self.address_type.to_bytes(1, "big") \
                + bytes_address(self.bind_host, self.address_type) + self.bind_port.to_bytes(2, "big")



class ConnectionReply(Reply):
    def __init__(self, version: int, method: int) -> None:
        self.version = version
        self.method = method

    def to_bytes(self) -> bytes:
        return self.version.to_bytes(1, "big") + self.method.to_bytes(1, "big")


class AuthenticationReply(Reply):
    def __init__(self, version: int, status: int):
        self.version = version
        self.status = status

    def to_bytes(self) -> bytes:
        return self.version.to_bytes(1, "big") + self.status.to_bytes(1, "big")