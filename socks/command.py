import socket
import errno
import select
from .request import Request
from .reply import Reply
from .constants import BUFFER_SIZE, AddressType, ReplyStatus, Command
from .session import Session


def handle_request(conn: socket.socket, session: Session):
    request = conn.recv(BUFFER_SIZE)
    if len(request) == 0:
        print(f"[INFO] {session.addr} closed connection")
        return False

    ver, cmd, rsv, atyp, dst_addr, dst_port = Request(request).decode()
    if not session.is_auth:
        reply = Reply(ver, ReplyStatus.CONNECTION_NOT_ALLOWED_BY_RULESET, rsv, atyp, dst_addr, dst_port).encode()
        conn.sendall(reply)
        return False

    if cmd == Command.CONNECT:
        command = ConnectCommand(conn, atyp, dst_addr, dst_port)
        rep = command.connect_dst()
        reply = Reply(ver, rep, rsv, atyp, dst_addr, dst_port).encode()
        conn.sendall(reply)
        command.forward()

    elif cmd == Command.BIND:
        first_reply = (ver, command, rsv, dst_addr, dst_port).encode()
        conn.sendall(first_reply)

        command = ConnectCommand(conn, atyp, dst_addr, dst_port)
        rep = command.connect_dst()

        if rep == ReplyStatus.SUCCEEDED():
            second_reply = (ver, rep, rsv).encode()
            conn.sendall(second_reply)
            command.forward()

        else:
            second_reply = (ver, rep, rsv).encode()
            conn.sendall(second_reply)
            command.forward()

    elif cmd == Command.UDP_ASSOCIATED:
        pass

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
