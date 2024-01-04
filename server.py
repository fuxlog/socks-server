import socket
import threading
from socks.connection import Connection
from socks.session import Session
from socks.authenticate import UsernamePasswordAuthentication
from socks.command import handle_request
from config import SERVER_HOST, SERVER_PORT, SERVER_BACKLOG



def handle_client(client, address):
    session = Session(client=client, address=address)
    session.notify()

    connection = Connection(session)
    if connection.connect() is True:
        session.notify_connection_success
        authentication = UsernamePasswordAuthentication(session)
        session.is_auth = authentication.authenticate()
        # session.is_auth = True
        if session.is_auth is True:
            session.notify_authentication_success()
            handle_request(session)
        else:
            session.notify_authentication_failed()
            return
    else:
        session.notify_connection_failed()    
        return


def run(server_address):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    server.listen(SERVER_BACKLOG)
    print(f"[START] Server {server_address} is running")
    while True:
        client, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, address, ))
        client_handler.start()


if __name__ == '__main__':
    run((SERVER_HOST, SERVER_PORT))

