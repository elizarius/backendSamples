import socket

hostname = socket.gethostname()
print socket.gethostbyname(hostname)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(("localhost", 1234))

print clientsocket.recv(1024)