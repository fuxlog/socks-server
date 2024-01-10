import socket
from .constants import PUBLIC_KEY
import logging

class Session:
    def __init__(self, client: socket.socket, address) -> None:
        self.client = client
        self.address = address
        self.is_auth = False
        self.key = PUBLIC_KEY

    def notify(self):
        print(f"[INFO] Client {self.address} want to make connection")
        logging.info(f"Client {self.address} want to make connection")
    
    def notify_connection_success(self):
        print(f"[INFO] Client {self.address} connection success")
        logging.info(f"Client {self.address} connection success")

    def notify_connection_failed(self):
        print(f"[INFO] Client {self.address} connection failed")
        logging.info(f"Client {self.address} connection failed")

    def notify_authentication_success(self):
        print(f"[INFO] Client {self.address} login success")
        logging.info(f"Client {self.address} login success")
    
    def notify_authentication_failed(self):
        print(f"[INFO] Client {self.address} login failed")
        logging.info(f"Client {self.address} login failed")

    def notify_register_success(self):
        print(f"[INFO] Client {self.address} register success")
        logging.info(f"Client {self.address} register success")
 
    def notify_register_failed(self):
        print(f"[INFO] Client {self.address} register failed")
        logging.info(f"Client {self.address} register failed")
 
    def notify_modified_success(self):
        print(f"[INFO] Client {self.address} change password success")
        logging.info(f"Client {self.address} change password success")
 
    def notify_modified_failed(self):
        print(f"[INFO] Client {self.address} change password failed")
        logging.info(f"Client {self.address} change password failed")
