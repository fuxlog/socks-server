import socket


class Session:
    def __init__(self, client: socket.socket, address) -> None:
        self.client = client
        self.address = address
        self.is_auth = False

    def notify(self):
        print(f"[INFO] Client {self.address} want to make connection")
    
    def notify_connection_success(self):
        print(f"[INFO] Client {self.address} connection success")

    def notify_connection_failed(self):
        print(f"[INFO] Client {self.address} connection failed")

    def notify_authentication_success(self):
        print(f"[INFO] Client {self.address} login success")
    
    def notify_authentication_failed(self):
        print(f"[INFO] Client {self.address} login failed")