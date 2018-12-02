#!/usr/bin/env python
import binascii

text = "hello, mrs teal"

data = binascii.a2b_base64(text)
print (text, "<=>", data)

data = binascii.b2a_base64(data)
print (text, "<=>", data)

t1 = binascii.a2b_base64(data)
print (t1, "<=>", data)

data = binascii.b2a_uu(text)
print text, "<=>", repr(data)

t2 = binascii.a2b_uu(data)
print t2, "<=>", repr(data)

#data = binascii.b2a_hqx(text)
#text = binascii.a2b_hqx(data)[0]
#print text, "<=>", repr(data)

# 2.0 and newer
#data = binascii.b2a_hex(text)
#text = binascii.a2b_hex(data)
#print text, "<=>", repr(data)

## hello, mrs teal <=> 'aGVsbG8sIG1ycyB0ZWFs\012'
## hello, mrs teal <=> '/:&5L;&\\L(&UR<R!T96%L\012'
## hello, mrs teal <=> 'D\'9XE\'mX)\'ebFb"dC@&X'
## hello, mrs teal <=> '68656c6c6f2c206d7273207465616c'
