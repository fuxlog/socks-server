from .constants import General, AddressType, Command, ReplyStatus
from .utils import str_address, int_port


class Request:
    def __init__(self):
        self.version = None
        self.command = None
        self.reserved = None
        self.address_type = None
        self.destination_host = None
        self.destination_port = None


    def from_bytes(self, data: bytes):
        if len(data) < 9 or len(data) > 260:
            return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE
        
        self.version = data[0]
        if self.version != General.VERSION:
            return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE

        self.command = data[1]
        if self.command != Command.CONNECT and self.command != Command.BIND and self.command != Command.UDP_ASSOCIATED:
            return ReplyStatus.COMMAND_NOT_SUPPORTED

        self.reserved = data[2]
        if self.reserved != 0:
            return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE
        
        self.address_type = data[3]

        ldata = len(data)
        if self.address_type == AddressType.IPV4:
            if ldata != 10:
                return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE
            self.destination_host = str_address(data[4:8], self.address_type)
            self.destination_port = int_port(data[8:10])
        elif self.address_type == AddressType.IPV6:
            if ldata != 22:
                return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE
            self.destination_host = str_address(data[4:20], self.address_type)
            self.destination_port = int_port(data[20:22])
        elif self.address_type == AddressType.DOMAINNAME:
            ldomain = data[4]
            if ldata != 7 + ldomain:
                return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE
            self.destination_host = str_address(data[4:5+ldomain], self.address_type)
            self.destination_port = int_port(data[ldata-2:ldata])
        else:
            return ReplyStatus.ADDRESS_TYPE_NOT_SUPPORTED
        
        return ReplyStatus.SUCCEEDED




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
