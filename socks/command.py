
import socket
import errno
import select
from .request import Request
from .reply import Reply
from .constants import BUFFER_SIZE, AddressType, ReplyStatus, Command, ReplyStatus
from .session import Session


def handle_request(session: Session):
    data = session.client.recv(BUFFER_SIZE)
    if len(data) == 0:
        print(f"[INFO] {session.addr} closed connection")
        return False

    request = Request()
    check_request_status = request.from_bytes(data)
    if not session.is_auth:
        reply = Reply(request.version, ReplyStatus.CONNECTION_NOT_ALLOWED_BY_RULESET, 
                      request.reserved, request.address_type, request.destination_host, request.destination_port)
        session.client.sendall(reply.to_bytes())
        return False
    
    if check_request_status != ReplyStatus.SUCCEEDED:
        reply = Reply(request.version, check_request_status, 
                      request.reserved, request.address_type, request.destination_host, request.destination_port)
        session.client.sendall(reply.to_bytes())
        return False

    if request.command == Command.CONNECT:
        command = ConnectCommand(session.client, request.destination_host, request.destination_port)
        reply_status = command.connect_dst()
        reply = Reply(request.version, reply_status, request.reserved, request.address_type, request.destination_host, request.destination_port)
        session.client.sendall(reply.to_bytes())
        command.forward()

    return True


def forward_data(src: socket.socket, dst: socket.socket):
    data = src.recv(BUFFER_SIZE)
    if not data:
        return False
    else:
        dst.sendall(data)
        return True


class ConnectCommand:
    def __init__(self, client_socket: socket.socket, atyp: int, dst_addr: str, dst_port: int):
        self.client_socket = client_socket
        self.target_socket: socket.socket = None
        self.atyp = atyp
        self.dst_addr = dst_addr
        self.dst_port = dst_port

    def connect_dst(self):
        print(f"[INFO] Connecting to destination {self.dst_addr}:{self.dst_port}")
        try:
            if self.atyp == AddressType.IPV4():
                target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.atyp == AddressType.IPV6():
                target = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            elif self.atyp == AddressType.DOMAINNAME():
                self.dst_addr = socket.gethostbyname(self.dst_addr)
                target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target.connect((self.dst_addr, self.dst_port))
            self.target_socket = target
            return ReplyStatus.SUCCEEDED()
        except socket.error as e:
            if isinstance(e, socket.timeout):
                return ReplyStatus.TTL_EXPIRED
            elif e.errno == errno.ECONNREFUSED:
                return ReplyStatus.CONNECTION_REFUSED
            else:
                return ReplyStatus.GENERAL_SOCKS_SERVER_FAILURE

    def forward(self):
        inputs = [self.client_socket, self.target_socket]
        while inputs:
            readable, _, _ = select.select(inputs, [], [])
            for ready_socket in readable:
                if ready_socket == self.target_socket:
                    success = forward_data(ready_socket, self.client_socket)
                if ready_socket == self.client_socket:
                    success = forward_data(ready_socket, self.target_socket)
                if not success:
                    print(f"[INFO] Connection closed")
                    self.target_socket.close()
                    break
            if self.target_socket.fileno() == -1:
                break
