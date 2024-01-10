
import socket
import errno
import select
from .request import Request
from .reply import Reply
from .constants import BUFFER_SIZE, AddressType, ReplyStatus, Command, ReplyStatus
from .session import Session
from .cryption import send_encrypted, recv_decrypted, CryptoRequest, CryptoReply
from cryptography.exceptions import InvalidTag


def handle_request(session: Session):
    data = recv_decrypted(session=session)
    if data is None:
        print(f"[INFO] {session.address} closed connection")
        return False
    request = Request()
    check_request_status = request.from_bytes(data)
    if not session.is_auth:
        session.client.close()
        return 
    
    if check_request_status != 0:
        session.client.close()
        return False

    if request.command == Command.CONNECT:
        command = ConnectCommand(session, session.client, request.address_type, request.destination_host, request.destination_port)
        reply_status = command.connect_dst()
        reply = Reply(request.version, reply_status, request.reserved, request.address_type, request.destination_host, request.destination_port)
        send_encrypted(session=session, message=reply.to_bytes())
        command.forward()
    elif request.command == Command.BIND:
        print("THIS IS BIND COMMAND")
    elif request.command == Command.UDP_ASSOCIATED:
        print("THIS IS UDP ASSOCIATED COMMAND")


# Mode 1 is target to proxy to client
# Mode 0 is client to target
def forward_data(src: socket.socket, dst: socket.socket, session: Session, mode):
    if not session.is_auth:
        return False

    if mode == 0:
        try:
            bl_message = src.recv(2)
            l_message = int.from_bytes(bl_message, "big")
            message = src.recv(l_message)
            if not message:
                return False
        
            request = CryptoRequest(session=session)
            if not request.from_bytes(message):
                return False
        
            dst.sendall(request.data)
        except socket.error:
            return False
    
    else:
        data = src.recv(BUFFER_SIZE)
        if not data:
            return False
        
        reply = CryptoReply(session=session)
        try:
            message = reply.to_bytes(data)
            l_message = len(message)
            dst.sendall(l_message.to_bytes(2, "big"))
            dst.sendall(message)
        except socket.error:
            return False

    return True


class ConnectCommand:
    def __init__(self, session: Session, client_socket: socket.socket, atyp: int, dst_addr: str, dst_port: int):
        self.session = session
        self.client_socket = client_socket
        self.target_socket: socket.socket = None
        self.atyp = atyp
        self.dst_addr = dst_addr
        self.dst_port = dst_port

    def connect_dst(self):
        print(f"[INFO] {self.session.address} Connecting to destination {self.dst_addr}:{self.dst_port}")
        try:
            if self.atyp == AddressType.IPV4:
                target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.atyp == AddressType.IPV6:
                target = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            elif self.atyp == AddressType.DOMAINNAME:
                self.dst_addr = socket.gethostbyname(self.dst_addr)
                target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target.connect((self.dst_addr, self.dst_port))
            self.target_socket = target
            return ReplyStatus.SUCCEEDED
        except socket.error as e:
            if isinstance(e, socket.timeout):
                return ReplyStatus.TTL_EXPIRED
            elif e.errno == errno.ECONNREFUSED:
                return ReplyStatus.CONNECTION_REFUSED
            else:
                return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE

    def forward(self):
        try:
            if self.client_socket is None or self.target_socket is None:
                return
            
            inputs = [self.client_socket, self.target_socket]
            while inputs:
                readable, _, _ = select.select(inputs, [], [])
                for ready_socket in readable:
                    if ready_socket == self.target_socket:
                        success = forward_data(ready_socket, self.client_socket, self.session, 1)
                    if ready_socket == self.client_socket:
                        success = forward_data(ready_socket, self.target_socket, self.session, 0)
                    if not success:
                        print(f"[INFO] {self.session.address} Connection closed forwarding tunnel")
                        self.target_socket.close()
                        break
                    if self.target_socket.fileno() == -1:
                        break
        except select.error as e:
            return
        except ValueError as e:
            return