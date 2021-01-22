#!/usr/bin/python

"""
Terminology:
 
- Object:       everything in python is object 
- Type:         type of object type(x)
- Attribute:    data members of type or class dir(X) in terms C++  --> hasattr
- Properties:   special attributes, like  __get__, __set__, __delete__ , 
                f.i. used to limit access to  attributes if want to make attr private.
                See classProperties_ss.py
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
    
    def __repr__(self):
        return('Animal representation: {} : {} : {}'.format(self.name,
                                                            self.color, 
                                                            self.age))


    def get_name(self):
        return(self.name)

    # classmethod works on level of class but not instance
    @classmethod  
    def print_animal(cls):
        print('ANIMAL FUNCTION')


# 1. Class attributes (properties) of class
an = Animal()
print('\n*  Attributes of Class instance ')
print (vars(an))

print('\n*  Class representation (__repr__)')
print (repr(an))

print('\n*  Class representation by string (__str__)')
print (str(an))



print('\n*  Attributes of Class ')
print (vars(Animal))

# 2. Class and type operations
a = 1
print('\n** Type int: {} '.format(type(a)))
print('\n** Type list: {} '.format(type([])))

print('** Type of Animal instance: {} '.format(type(an)))
print('** Type of Animal class: {} '.format(type(Animal)))
print('** Type of Animal class name: {} '.format(an.__class__))
print('\n** Convert Animal class to dict: {} '.format(an.__dict__))

print('\n** Animal Other attr: {} '.format(an.__module__))
# print class name via __str__ method
print('\n** Animal str attr: {} '.format(an.__str__()))
print('** Animal instance name: {} '.format(an))

# 3. Class initialization

# Note: @classmethod / cls used to implemented inheritance
print('\n***    Age,, global class member: {} '.format(an.age))


# 4. Class inheritance
print('\n\n ************  Class Inheritance Demo **********')

class Horse(Animal):

    def __init__(self , legs=4):
        self.legs = legs
        self.name = 'DIMKABUKASUKA'
        print('HORSE init called')
        # Base class init is not called by default. Could be:
        # Animal.__init(self, ...)

    def __str__(self):
        return('AELZ Horse inherited')

horse = Horse(legs=8)                                       # base class init is not called by default
print('** Inheritance: {} '.format(horse))
print('** N of legs: {} '.format(horse.legs))
print('** Horse age: {} '.format(horse.age))                # global class static attribute 
horse.print_animal()
print('** Horse name : {} '.format(horse.get_name()))       # function from global class method


print('\n** Horse hierarchy help function ** \n')
#help(horse)
print('\n** Subclass checking: {} \n'.format(issubclass(Horse, Animal)))



print('\n\n ************  Multiple Inheritance Demo **********')
class Father:
    pass

class Mother:
    pass

class Child1(Father, Mother):
    pass

#help(Child1)


print('\n\n ************  Polymorphism Demo: function overriding **********')
class Base:
    def print_method(self):
        print('I am BASE')

    def print_base(self):
        print('I am BASE BASE BASE')


class Der1(Base):
    def print_method(self):
        print('I am DER_111')


class Der2(Base):
    def print_method(self):
        print('I am DER_222')

bas = Base()
bas.print_method()
d1 = Der1()
d1.print_method()
d2 = Der2()
d2.print_method()
d2.print_base()

print('\n\n ************  Special Methods  **********')

