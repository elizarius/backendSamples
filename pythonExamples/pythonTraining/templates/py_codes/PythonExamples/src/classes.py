class Person :
    # Class variable declarations
    name = ""
    address = ""
 
    # Class method definitions
    def __init__(self, name, address) :
        self.name = name
        self.address = address
 
    def tell(self) :
        print self.name , self.address


p = Person("Ben", "A St 3")
p.tell()
