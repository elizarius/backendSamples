#!/usr/bin/python

"""
Terminology:
 
- Object:       everything in python is object 
- Type:         type of object type(x)
- Attribute:    data members of type or class dir(X) in terms C++   --> hasattr
- Properties:   special attributes, like  __get__, __set__, __delete__ , 
                f.i. used to limit access to  attributes if want to make attr private
- Method:       data functions in terms C++ 
"""

class Animal(object):
    age = 25

    def __init__(self):
        self.legs = 2
        self.name = 'Dog'
        self.color= 'Spotted'
        self.smell= 'Alot'
        self.age  = 10
        self.kids = 0
        print('Animal init called')

    def __str__(self):
        return('AELZ animal')

    def get_name(self):
        return(self.name)

    @classmethod
    def print_animal(cls):
        print('ANIMAL FUNCTION')


# 1. Class attributes (properties) of class
an = Animal()
attrs =vars(an)
print('\n*  example')
print (attrs)
print (vars(Animal))

# 2. Class and type operations
a = 1
print('\n** Type int: {} '.format(type(a)))
print('\n** Type list: {} '.format(type([])))

print('** Type of Animal instance: {} '.format(type(an)))
print('** Type of Animal instance: {} '.format(type(Animal)))
print('** Type of Animal class name: {} '.format(an.__class__))
print('\n** Convert Animal class to dict: {} '.format(an.__dict__))
print('\n** Animal Other attr: {} '.format(an.__module__))
# print class name via __str__ method
print('\n** Animal str attr: {} '.format(an.__str__()))
print('** Animal instance name: {} '.format(an))

# 3. Class initialization

# Note: @classmethod / cls used to implemented inheritnce
print('\n***    Age,, global class member: {} '.format(an.age))


# 4. Class inheritance
print('\n\n ************ Class Inheritance Demo **********')


class Horse(Animal):

    def __init__(self , legs=4):
        self.legs = legs
        self.name = 'DIMKABUKASUKA'

    def __str__(self):
        return('AELZ Horse inherited')

horse = Horse(legs=8)                           # base class init is not called
print('** Inheritance: {} '.format(horse))
print('** N of legs: {} '.format(horse.legs))
print('** Horse age: {} '.format(horse.age))    # from global class method
print('** Call parent: {} '.format(horse.print_animal()))
print('** Horse name : {} '.format(horse.get_name()))    # from global class method
