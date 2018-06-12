import xmlrpclib

server = xmlrpclib.ServerProxy("http://betty.userland.com:80")

print server.examples.getStateName(5)

stateObject = server.examples
print stateObject.getStateName(50)