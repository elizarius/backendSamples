#!/usr/bin/env python
import traceback

class   Setter(object):
    key_1 = '11111111'
    key_2 = '22222222'

    @staticmethod
    def getKey_1():
        print ("getKey_1 %s" % Setter.key_1)
        return Setter.key_1

    @staticmethod
    def setKey_1(value):
        if value == '12345':
            raise Exception ('AELZ setting KEY method')
        Setter.key_1 = value
        print ("setKey_1   %s" % Setter.key_1)
        return Setter.key_1

try:
    zz = Setter.getKey_1()
    pwd='12345'
    Setter.setKey_1(pwd)

except Exception as e:
    print ("AELZ IN exception %s " % zz)
    msg = "Getting of base_key failed: {}".format(str(e))
    print("{0} : {1}".format(msg, traceback.format_exc()))


print("AELZ finalizing after exception")




