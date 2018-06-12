#!/usr/bin/python

import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("localhost", 1234))
serversocket.listen(1)

(clientsocket, address) = serversocket.accept()
print address
clientsocket.send('hello!')
