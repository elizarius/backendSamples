#!/usr/bin/env python
import socket

print('*** Creating client ***')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP SOCKET 
s.connect((socket.gethostname(), 4571))
msg = s.recv(1024)
print('*** Message from server: {}'.format(msg.decode('utf-8')))
s.close()
