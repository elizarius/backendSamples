#!/usr/bin/env python
import sys
import httplib


nf = httplib.NOT_FOUND
ok = httplib.OK


#print("Http status %s , %s" % (nf.reason, ok.reason))
print("Http status %s , %s" % (nf, ok))
print("Http status {0},{1}".format(nf, ok))


