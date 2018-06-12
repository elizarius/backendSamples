#!/usr/bin/env python

class   Setter(object):
    key_1 = '11111111'
    key_2 = '22222222'

    @staticmethod
    def getKey_1():
        print ("getKey_1 %s" % Setter.key_1)
        return Setter.key_1

    @staticmethod
    def setKey_1(value):
        Setter.key_1 = value
        print ("setKey_1   %s" % Setter.key_1)
        return Setter.key_1

zz = Setter.getKey_1()
print ("ZZ:  %s" % zz)

Setter.setKey_1('3333333')
print ("ZZ:  %s" % Setter.getKey_1())

Setter().setKey_1('44444444')
print ("ZZ:  %s" % Setter.getKey_1())

