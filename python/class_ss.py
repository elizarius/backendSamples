#!/usr/bin/python

"""
Terminology:
 
- Object:       everything in python is object 
- Type:         type of object type(x)
- Class         class is type as usuual in OOP
- Attribute:    data members of type or class dir(X) in terms C++  --> hasattr
- Properties:   special attributes, that have   __get__, __set__, __delete__ methods,see classProperty_ss.py
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

    def __add__(self, other):
        return(self.age + other)


    def get_name(self):
        return(self.name)

    # classmethod works on level of class but not instance
    @classmethod  
    def print_animal(cls):
        print('ANIMAL FUNCTION')


an = Animal()
print('\n*  Instance Attributes')
print (vars(an))

print('\n*  Class Attributes')
print (vars(Animal))

print('\n*  Class representation (__repr__)')
print (repr(an))

print('\n*  Class representation by string (__str__)')
print (str(an))



print('\n*  ***** Class and type representations **** ')
a = 1
print('\n** Type int: {} '.format(type(a)))
print('\n** Type list: {} '.format(type([])))

print('** Type of Animal instance: {} '.format(type(an)))
print('** Type of Animal class: {} '.format(type(Animal)))
print('** Type of Animal class name: {} '.format(an.__class__))


print('\n** Convert Animal instance to dict: {} '.format(an.__dict__))

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



print('\n ***  Builtin (internal attr) of INT type) ***\n')
print(vars(int))

z = 1+2
k = int.__add__(1, 2)
print('\n{} : {}'.format(z,k))
# AELZ_01 important, operations +,- event for int types implemented as attributes __add__, __sub__
# Same meethod can be implemented for custom classes, see Animal._add f.i 
# (//, __floordiv__)--> celochislennoe delenie, 
# (%, __mod__) --> ostatok ot delenija , modulo
# ( **,  __pow__) --> vozvedenuije v stepen' 

