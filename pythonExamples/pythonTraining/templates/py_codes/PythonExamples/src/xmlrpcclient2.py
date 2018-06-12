#! /usr/bin/python

# xmlrpcclient.py
# XML-RPC client example
# Copyright Tieturi Oy 2009

import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:4321/")

print "Sum of 12 and 14 is",  str(proxy.sum(12,14))   
