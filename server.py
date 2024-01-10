import socket
import threading
import sys
from socks.connection import Connection
from socks.session import Session
from socks.authenticate import UsernamePasswordAuthentication
from socks.command import handle_request
from socks.constants import General
from config import SERVER_HOST, SERVER_PORT, SERVER_BACKLOG
import logging


logging.basicConfig(filename='server.log', level=logging.INFO, format='[%(levelname)s] - %(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


def handle_client(client, address):
    session = Session(client=client, address=address)
 
    connection = Connection(session)
    if connection.connect() is True:
        session.notify_connection_success()
        authentication = UsernamePasswordAuthentication(session)
        session.is_auth, version = authentication.authenticate()
        if version == General.AUTHENTICATION_VERSION:
            if session.is_auth is False:
                session.notify_authentication_failed()
                return
            session.notify_authentication_success()
            handle_request(session)
 
        elif version == General.REGISTER_VERSION:
            if session.is_auth is False:
                session.notify_register_failed()
            else: 
                session.notify_register_success()
            return
        
        elif version == General.MODIFIED_VERSION:
            if session.is_auth is False:
                session.notify_modified_failed()
            else:
                session.notify_modified_success()
            return
           
    else:
        session.notify_connection_failed()    
        return


def run(server_address):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    server.listen(SERVER_BACKLOG)
    print(f"[START] Server is listening {server_address[0]}:{server_address[1]}")
    logging.info(f"Server start listening on {server_address[0]}:{server_address[1]}")
    while True:
        client, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, address, ))
        client_handler.start()


if __name__ == '__main__':
    try:
        run((SERVER_HOST, SERVER_PORT))
    except KeyboardInterrupt:
        print(f"\n[INFO] Server {SERVER_HOST}:{SERVER_PORT} is shutting down")
        logging.info(f"Server {SERVER_HOST}:{SERVER_PORT} is shutting down")
        sys.exit(1)

