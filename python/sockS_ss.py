#!/usr/bin/env python
import socket
print('Host name: {}'.format(socket.gethostname()))
print('Host by name 1: {}'.format(socket.gethostbyname('localhost')))
print('Host by name 2: {}'.format(socket.gethostbyname(socket.gethostname())))
print('Host by addr 1: {}'.format(socket.gethostbyaddr('127.0.0.1')))
print('Host by addr 2: {}'.format(socket.gethostbyaddr('127.0.1.1')))

print('Host by name 3: {}'.format(socket.gethostbyname('')))


print('*** Creating server ***')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP SOCKET 
s.bind((socket.gethostname(), 4571))
s.listen(5)

print('*** Server is up. Listening for connections***')
client, address = s.accept()

print(f'*** Connection to {address} established ***')
print(f'*** Client object {client} ***')
client.send(bytes('Hello! Alex ', 'utf-8'))
s.close()