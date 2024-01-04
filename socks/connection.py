from .constants import BUFFER_SIZE, General, Method
from .session import Session
from .request import ConnectionRequest
from .reply import ConnectionReply


def validate(version, methods) -> int:
    """ 
    Compare client's version/methods request with server's version/methods.

    Server only use USERNAME/PASSWORD for authenticate or register method.

    """
    if version != General.VERSION:
        return Method.NO_ACCEPTABLE_METHOD
    
    if Method.USERNAME_PASSWORD in methods:
        return Method.USERNAME_PASSWORD
    
    # if Method.NO_AUTHENTICATION_REQUIRED in methods:
    #     return Method.NO_AUTHENTICATION_REQUIRED

    else:
        return Method.NO_ACCEPTABLE_METHOD


class Connection:
    def __init__(self, session: Session):
        self.session = session

    def connect(self):
        data = self.session.client.recv(BUFFER_SIZE)
        print(data)

        request = ConnectionRequest()
        if request.from_bytes(data):
            method_chosen = validate(request.version, request.methods)                
            reply = ConnectionReply(version=request.version, method=method_chosen)
            self.session.client.sendall(reply.to_bytes())
            if method_chosen == Method.NO_ACCEPTABLE_METHOD:
                self.session.client.close()
                return False
            return True

        # Request format is not acceptable according to SOCKS5
        reply = ConnectionReply(version=General.VERSION, method=Method.NO_ACCEPTABLE_METHOD)
        self.session.client.sendall(reply.to_bytes())
        self.session.client.close()
        return False
