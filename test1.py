import socket
from config import SERVER_HOST, SERVER_PORT


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER_HOST, SERVER_PORT))

server.sendall(b"\x05\x031\x0fgagasdgasdgasdga2")
data = server.recv(1024)
if not data:
    server.close()
    
print(data)

server.sendall(b"\x01\x05admin\x09admin202f")
data = server.recv(1024)
print(data)