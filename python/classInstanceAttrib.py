#!/usr/bin/env python



class   Setter(object):
    key_1 = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    def __init__(self, instance_attr):
        self.key_1 = instance_attr

    def print_class_attr(self):
        print ("Class attribute from instance:  {}".format(Setter.key_1))

    def set_class_attr(self):
        Setter.key_1  = "YYYYYYYYYYYYYYYYYYYYY"


s1 = Setter('SET 111')
print ("Instance attribute:  {}".format(s1.key_1))
print ("Global class attribute:  {}".format(Setter.key_1))


s2 = Setter('SET 222222')
print ("Instance attribute:  {}".format(s2.key_1))
print ("Global class attribute:  {}".format(Setter.key_1))

s1.print_class_attr()
s2.print_class_attr()

Setter.key_1 = "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
s1.print_class_attr()
s2.print_class_attr()


s1.set_class_attr()
s1.print_class_attr()
s2.print_class_attr()



#print ("Printing as dictionaries:  {}".format(str(Setter.__dict__)))
#s1.ke1 = 
