#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html

from queue import Queue, LifoQueue, PriorityQueue
import time


q = Queue()
for i in range(7):
    q.put(i)

print('** 1. Queue demo FIFO thread safe !!! **')
print(q.queue)

# get all elements: FIFO: 
while not q.empty():
    print(q.get())


print('\n** 2.  Stack (LIFO) thread safe !!! **')
q = LifoQueue()
for i in range(7):
    q.put(i)

# get all elements: FIFO: 
while not q.empty():
    print(q.get())


print('\n** 3.  Priority queue thread safe !!! **')
# Could be used for sorting 
q = PriorityQueue()
q.put(5)
q.put(4)
q.put(1)
q.put(3)
q.put(2)

# Highest prio (=1) removed first from queue
while not q.empty():
    print(q.get())
