#! /usr/bin/python

# inheritance.py
# Exercise 10 & 11
# Copyright Tieturi Oy 2009

class Person :
    # Class variable declarations
    name = ""
    age = 0
    location = ""
 
    # Class method definitions
    def __init__(self, name, location, age) :
        self.name = name
        #should have similar check on age as the setAge() has
        self.age = age
        self.location = location
 
    def tell(self) :
        print self.name , self.location, self.age
        
    def setName(self, name):
        self.name = name
    
    def setAge(self, age):
        "age must be between 0 and 150"
        if age <= 0:
            self.age = 0
        elif age > 150:
            self.age = 150
        else:
            self.age = age
    
    def moveTo(self, location):
        self.location = location
        
    def getName(self):
        return self.name
    
    def getAge(self):
        return self.age
    
    def getLocation(self):
        return self.location
    
    #end of class Person
    
#class Employee
class Employee(Person) :
    title = ""
    salary = 0.0
    busphone = ""

    def __init__(self, name, location, age, title, salary, phone) :
        #initialize the base class
        Person.__init__(self, name, location, age)
        self.title = title
        self.salary = salary
        self.busphone = phone

    def __del__(self) :
        print "Destructor: ", self

    def printBusinesscard(self) :
        Person.tell(self)
        print self.title
        print self.salary
        print self.busphone

    def getTitle(self):
        return self.title
    
    def getSalary(self):
        return self.salary
    
    def getNumber(self):
        return self.busphone
    
    def setTitle(self, title):
        self.title = title
        
    def setSalary(self, salary):
        self.salary = salary
        
    def setPhone(self, phone):
        self.busphone = phone

        #end of class Employee
print "Person: ",
p = Person("John", "Helsinki", 37)
p.tell()
print "\nEmployee: ",
e = Employee("Darryll", "Tampere", 45, "Developer", 6700, "04055555555")
e.printBusinesscard()