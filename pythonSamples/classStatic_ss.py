#!/usr/bin/env python
class   Setter(object):
    key_1 = 'XXXX'

    def __init__(self, instance_attr):
        self.key_1 = instance_attr
        self.key_11 = instance_attr


    @staticmethod
    def get_global_key():       
        return Setter.key_1
 #      return key_1   # no references(CLS), cannot access instance or class variables

    # cls is working level of class and instance attriubtes cannot be used
    @classmethod
    def get_class_key(cls):       # note: no references to
        return cls.key_1


    @classmethod
    def get_new_instance(cls, in_attr):       # note: no references to
        return cls(in_attr)


# 1. Global class and instance attributes (members)
s1 = Setter('SET 111')
print ("\nInstance attribute:  {}".format(s1.key_1))
print ("Global class attribute:  {}".format(Setter.key_1))

s2 = Setter('SET 222222')
print ("\nInstance attribute:  {}".format(s2.key_1))
print ("Global class attribute:  {}".format(Setter.key_1))

Setter.key_1 = "ZZZZ"
print ("\nInstance attribute:  {}".format(s2.key_1))
print ("Global class attribute:  {}".format(Setter.key_1))

print ("\n**2 Static method, global key: {}".format(Setter.get_global_key()))
print ("\n**2 Static method, global key: {}".format(Setter.get_global_key()))

print ("\n**3 Class method key:  {}".format(s1.get_class_key()))
print ("\n**4 Class method key:  {}".format(Setter.get_class_key()))

ns = Setter.get_new_instance('huy')
print ("\n**5 Create instance by class method, NS key:  {}".format(ns.key_1))

