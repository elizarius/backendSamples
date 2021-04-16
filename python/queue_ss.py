#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html

from queue import Queue

print('** 1.  Built in queue demo **')
olympics =Queue(5)
olympics.put('US')
olympics.put('Zealand')
print ('Empty: {}  Full: {}'.format(olympics.empty(), olympics.full()))

item = olympics.get()
print ('Item  {} '.format(item))


print('\n** 2.  Stack (LIFO) demo **')
stack = []
stack.append('USA')
stack.append('GB')
stack.append('China')
print('** Stack: {} '.format(stack))
print('** Stack pop: {} '.format(stack.pop()))


print('\n** 3.  Linked list  **')

class Node:
    """
    A single-linked node
    """
    def __init__(self, dataval=None, nextval=None):
        self.dataval = dataval
        self.nextval = nextval

    def __repr__(self):
        return repr(self.dataval)


class LinkedList:
    """
    A single-linked list
    """
    def __init__(self):
        self.head = None

    def prepend(self, dataval):
        """ Insert element in beg of the list O(1) """
        self.head = Node(dataval=dataval, nextval=self.head)

    def append(self, dataval):
        """ Insert element at the end of the list O(n) """
        if not self.head:
            self.head = Node(dataval=dataval)   # no nextval

        curr = self.head

        while curr.nextval:
            curr =curr.nextval

        curr.nextval = Node (dataval = dataval)

