# Example Echo server program
# 
import socket

HOSTNAME = ''       # localhost
PORTNUM = 54321    # Random port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOSTNAME, PORTNUM))
server.listen(1)    # Backlog size, number of queued connections, min 1
connection, address = server.accept() # connection accepted
print 'Connection from', address
while 1:
    data = connection.recv(1024)
    if not data: break
    connection.send(data)
connection.close()
