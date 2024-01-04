from .session import Session
from .constants import BUFFER_SIZE, General, AuthenticationStatus
from .request import AuthenticationRequest
from .reply import AuthenticationReply
from .db import verify_account


class Authentication:
    def __init__(self, session: Session):
        self.session = session

    def authenticate(self):
        pass


class UsernamePasswordAuthentication(Authentication):
    def authenticate(self):
        if self.session.client.fileno == -1:
            print(f"[INFO] Client {self.session.address} has close connection before")
            return

        if self.session.is_auth is True:
            print(f"[INFO] Client {self.session.address} already logged in")
            return
        
        data = self.session.client.recv(BUFFER_SIZE)
        request = AuthenticationRequest()
        if request.from_bytes(data) is True:
            if request.version == General.AUTHENTICATION_VERSION:
                status = verify_account(request.uname, request.pword)
                if status:
                    reply = AuthenticationReply(request.version, AuthenticationStatus.SUCCESS)
                    self.session.client.sendall(reply.to_bytes())
                    return True

        reply = AuthenticationReply(General.AUTHENTICATION_VERSION, AuthenticationStatus.FAILURE)
        self.session.client.sendall(reply.to_bytes())
        self.session.client.close()
        return False