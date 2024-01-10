from .session import Session
from .constants import BUFFER_SIZE, General, AuthenticationStatus
from .request import AuthenticationRequest
from .reply import AuthenticationReply
from .db import verify_account, save_account, change_password
from .cryption import send_encrypted, recv_decrypted


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
        
        data = recv_decrypted(self.session)
        request = AuthenticationRequest()
        if request.from_bytes(data) is True:
            if request.version == General.AUTHENTICATION_VERSION:
                status = verify_account(request.uname, request.pword)
                if status:
                    reply = AuthenticationReply(request.version, AuthenticationStatus.SUCCESS)
                    send_encrypted(session=self.session, message=reply.to_bytes())
                    self.session.key = request.pword
                    return True, request.version

                reply = AuthenticationReply(request.version, AuthenticationStatus.FAILURE)   
                
                
            elif request.version == General.REGISTER_VERSION:
                status = save_account(request.uname, request.pword)
                if status:
                    reply = AuthenticationReply(request.version, AuthenticationStatus.SUCCESS)
                    send_encrypted(session=self.session, message=reply.to_bytes())
                    return True, request.version
                
                reply = AuthenticationReply(request.version, AuthenticationStatus.FAILURE)
                send_encrypted(session=self.session, message=reply.to_bytes())
                return False, request.version

            elif request.version == General.MODIFIED_VERSION:
                status = verify_account(request.uname, request.pword)
                if not status:
                    reply = AuthenticationReply(request.version, AuthenticationStatus.FAILURE)
                    send_encrypted(session=self.session, message=reply.to_bytes())
                    return False, request.version

                reply = AuthenticationReply(request.version, AuthenticationStatus.SUCCESS)
                send_encrypted(session=self.session, message=reply.to_bytes())

                data_for_change = recv_decrypted(self.session)
                change_request = AuthenticationRequest()
                if change_request.from_bytes(data_for_change):
                    change_status = change_password(change_request.uname, change_request.pword)
                    if change_status:
                        reply = AuthenticationReply(request.version, AuthenticationStatus.SUCCESS)
                        send_encrypted(session=self.session, message=reply.to_bytes())
                        return True, request.version
                
                reply = AuthenticationReply(request.version, AuthenticationStatus.FAILURE)
                send_encrypted(session=self.session, message=reply.to_bytes())
                return False, request.version
                

        reply = AuthenticationReply(General.AUTHENTICATION_VERSION, AuthenticationStatus.FAILURE)
        send_encrypted(session=self.session, message=reply.to_bytes())
        self.session.client.close()
        return False, General.AUTHENTICATION_VERSION
