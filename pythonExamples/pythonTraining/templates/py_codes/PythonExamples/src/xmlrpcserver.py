#! /usr/bin/python

# xmlrpcserver.py
# XML-RPC server example
# Copyright Tieturi Oy 2010

#import xmlrpclib

import SimpleXMLRPCServer
# Also from SimpleXMLRPCServer import SimpleXMLRPCServer is possible
def sum(a,b):
    return a+b

calcserver = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 4321))
# Different import simplifies this: ....= SimpleXMLRPCServer(("localhost", 1234))

print "Localhost, port 1234"
calcserver.register_function(sum, "sum")

print "Starting to serve"
calcserver.serve_forever()
