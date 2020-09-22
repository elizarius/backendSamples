#!/usr/bin/env python
import sys
if sys.version_info < (3,):
    import httplib as httpstatus
else:
   from http import HTTPStatus as httpstatus




#nf = HTTPStatus.NOT_FOUND
#ok = HTTPStatus.OK

nf = httpstatus.NOT_FOUND
ok = httpstatus.OK

zz = httpstatus.OK

#print("Http status %s , %s" % (nf.value, ok.value))
print("Http status %s , %s" % (nf, ok))
print("Http status {0},{1}".format(nf, ok))

if zz == ok:
    print("Http OK {0}".format(ok))



