class Request:
    def cook():
        pass


class ConnectionRequest(Request):
    def __init__(self):
        self.version = None
        self.methods = None

    def from_bytes(self, data: bytes):
        if len(data) < 3:
            return False

        version = data[0]
        nmethods = data[1]

        last_byte_index = len(data)
        if last_byte_index - 2 != nmethods:
            return False

        methods = tuple(data[2:last_byte_index])
        methods = set(methods)

        self.version = version
        self.methods = methods

        return True


class AuthenticationRequest(Request):
    """ Format for authentication request

    VERSION: 1 byte
    ULEN: 1 byte
    UNAME: 1 to 255 byte
    PLEN: 1 byte
    PWORD: 1 to 255 byte
    """

    def __init__(self):
        self.version = 0
        self.ulen = 0
        self.uname = None
        self.plen = 0
        self.pword = None

    def from_bytes(self, data: bytes) -> bool:
        if len(data) < 5:
            return False

        self.version = data[0]
        self.ulen = data[1]
        if len(data) < 4 + self.ulen:
            return False

        self.uname = data[2: 2 + self.ulen].decode()
        self.plen = data[2 + self.ulen]
        if len(data) < 3 + self.ulen + self.plen:
            return False

        self.pword = data[3 + self.ulen: 3 + self.ulen + self.plen].decode()
        return True
