import socket
from .constants import PUBLIC_KEY
import logging

class Session:
    def __init__(self, client: socket.socket, address) -> None:
        self.client = client
        self.address = address
        self.is_auth = False
        self.key = PUBLIC_KEY
    
    def notify_connection_success(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]}  connection success")
        logging.info(f"{self.address[0]}:{self.address[1]}  connection success")

    def notify_connection_failed(self):
        print(f"[INFO] Client {self.address} connection failed")
        logging.info(f"Client {self.address} connection failed")

    def notify_authentication_success(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]} login success")
        logging.info(f"{self.address[0]}:{self.address[1]} login success")
    
    def notify_authentication_failed(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]} login failed")
        logging.info(f"{self.address[0]}:{self.address[1]} login failed")

    def notify_register_success(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]} register success")
        logging.info(f"{self.address[0]}:{self.address[1]} register success")
 
    def notify_register_failed(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]} register failed")
        logging.info(f"{self.address[0]}:{self.address[1]} register failed")
 
    def notify_modified_success(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]} change password success")
        logging.info(f"{self.address[0]}:{self.address[1]} change password success")
 
    def notify_modified_failed(self):
        print(f"[INFO] {self.address[0]}:{self.address[1]} change password failed")
        logging.info(f"{self.address[0]}:{self.address[1]} change password failed")
