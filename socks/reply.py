class Reply:
    def to_bytes(self):
        pass


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

    def to_bytes(self):
        return self.version.to_bytes(1, "big") + self.status.to_bytes(1, "big")
