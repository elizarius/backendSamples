#!/usr/bin/env python

from abc import ABC, abstractmethod

class   Setter(ABC):   # means class incomplete and has some empty methods
    key_1 = 'XXXX'

    def __init__(self, instance_attr):
        self.key_1 = instance_attr


    @abstractmethod
    def get_global_key():
        pass

    def get_class_key(cls):
        PASS

class   S2(Setter):
    def __init__(self, instance_attr):
        self.key_2 = instance_attr



    def get_global_key():
        return "Global"

    def get_class_key(cls):
        return "Class Ker2"


    @classmethod
    def get_new_instance(cls, in_attr):       # note: no references to
        return cls(in_attr)


# 1. Global class and instance attributes (members)
# If abstract method present, class cannot be instantiated but class attribute can be called!!!

#s1 = Setter('SET 111')  # If abst
# print ("\nInstance attribute:  {}".format(s1.key_1))
print ("Class attribute:  {}".format(Setter.key_1))

s2 = S2('kuku')
print(f'\n  S2 by dir {dir(s2)}')

print(f'\nABC vars : {vars(ABC)}')
print(f'\nABC DICT : {ABC.__dict__}')
print(f'\nABC type : {type(ABC)}')
print(f'\nABC representation : {repr(ABC)}')
print(f'\nABC dir  : {dir(ABC)}') ### !!!!!!! built in function



