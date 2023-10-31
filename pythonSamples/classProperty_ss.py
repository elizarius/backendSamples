#!/usr/bin/python

''' Documentation

Docstring format of documentation defined in PEP 257

'''

# @property is an encapsultor of data member to simplify get, set del functions 
#
class Animal(object):
    '''
    Docstring of class can be called from code
    '''
    age = 25

    def __init__(self):
        self._legs = 2

    # @pZZZZ also named decorator tappern
    @property       
    def legs(self):
        return(self._legs)

    # without setter assignment to property is not allowed
    @legs.setter
    def legs(self, val):
      self._legs = val

    @legs.deleter
    def legs(self):
        del self._legs


    # Note: property also might have getter, deleter, doc string
    # https://docs.python.org/3.6/library/functions.html#property

an = Animal()
print('\n** Property legs:  {} '.format(an.legs))
an.legs = 4
print('\n** Property legs:  {} '.format(an.legs))
print('\n** Legs:  {} '.format(an._legs))   # possible call method dicrectly, that is strange


print('\n** Buildins(properties) can be overloaded')
print(dir(an))

print(an.__dict__)

print(Animal.__dict__)


print(an.__doc__)
print(an.__str__)

#help(__name__)     # doc for main module
#help(an.__init__)  # doc for functions
#help(an)            # doc for animal class

