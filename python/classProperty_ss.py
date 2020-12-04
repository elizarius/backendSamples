#!/usr/bin/python

''' Documentation

Docstring format of documentation defined in PEP 257

'''

# Property is as private member to limit access to
# data member to be private
#
class Animal(object):
    '''
    Docstring of class can be called from code
    '''
    age = 25

    def __init__(self):
        self._legs = 2

    @property
    def legs(self):
        return(self._legs)

    # without setter assignment to property is not allowed
    @legs.setter
    def legs(self, val):
      self._legs = val

    # Note: property also might have getter, deleter, doc string
    # https://docs.python.org/3.6/library/functions.html#property

an = Animal()
print('\n** Property legs:  {} '.format(an.legs))
an.legs = 4
print('\n** Property legs:  {} '.format(an.legs))

#  Build in class methods can be overloaded
attrs = dir(an)

print('\n** Buildins can be overloaded')
print(attrs)

print(an.__doc__)
#help(__name__)     # doc for main module
#help(an.__init__)  # doc for functions
help(an)            # doc for animal class

