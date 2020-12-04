#!/usr/bin/env python
class   Setter(object):
    key_1 = 'XXXX'

    def __init__(self, instance_attr):
        self.key_1 = instance_attr

    @staticmethod
    def get_global_key():       # note: no references to
        return Setter.key_1


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

# 2. Static method
print ("\n** Class key by static method:  {}".format(Setter.get_global_key()))

