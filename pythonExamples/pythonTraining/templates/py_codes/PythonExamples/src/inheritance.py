#! /usr/bin/python

# inheritance.py
# class inheritance example
# Copyright Tieturi Oy 2009

class Person :
    name = ""
    address = ""
 
    def __init__(self, name, address) :
        self.name = name
        self.address = address
 
    def tell(self) :
        print self.name , self.address


class Employee(Person) :
    company = ""

    def __init__(self, name, address, company) :
        Person.__init__(self, name, address)
        self.company = company

    def __del__(self) :
        print "Destructor: ", self

    def tell(self) :
        Person.tell(self)
        print self.company

e = Employee("John", "Street", "Tieturi")
e.tell()

