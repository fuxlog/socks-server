BUFFER_SIZE = 4096


class Identifier:
    @staticmethod
    def VERSION():
        return 5

    @staticmethod
    def AUTHENTICATE_VERSION() -> int:
        return 1

    @staticmethod
    def REGISTER_VERSION():
        return 2


class Method:
    @staticmethod
    def NO_AUTHENTICATION_REQUIRED():
        return 0

    @staticmethod
    def GSSAPI():
        return 1

    @staticmethod
    def USERNAME_PASSWORD():
        return 2

    @staticmethod
    def NO_ACCEPTABLE_METHODS():
        return 255


class Command:
    @staticmethod
    def CONNECT():
        return 1

    @staticmethod
    def BIND():
        return 2

    @staticmethod
    def UDP_ASSOCIATED():
        return 3


class AddressType:
    @staticmethod
    def IPV4():
        return 1

    @staticmethod
    def DOMAINNAME():
        return 3

    @staticmethod
    def IPV6():
        return 4


class AuthenticationStatus:
    @staticmethod
    def SUCCESS():
        return 0

    @staticmethod
    def FAILURE():
        return 1
