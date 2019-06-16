#!/usr/bin/env python3

class ListExample:
    def __init__(self):
        numbersList = []
        pass

    def add_numbers(self, numbers):
        self.numbersList = numbers

    def add_number(self, number):
        self.numbersList.append(number)

    def print_numbers(self):
        print ("NumbersList: {}".format(self.numbersList))

    def get_total(self):
        return sum(self.numbersList)

    def get_last_3(self):
        new_list = self.numbersList[-3:]
        return sum(new_list)

ll = ListExample()
ll.add_numbers([1,2,3])
ll.print_numbers()
print ("Total: {}".format(ll.get_total()))
print ("Last_3 sum_1   {}".format(ll.get_last_3()))
print ("***********************")
print (" ")

ll.add_number(8)
ll.print_numbers()
print ("Total: {}".format(ll.get_total()))
print ("Last_3 sum_2:  {}".format(ll.get_last_3()))
