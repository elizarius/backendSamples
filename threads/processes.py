#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html

import time
import os
from multiprocessing import Process,current_process

def square(n):
    time.sleep(1)
    result = n * n
    p_id = current_process().pid
    p_name = current_process().name
    print(f'Process ID:  {p_id} Name: {p_name}')
    print(f'The number {n} squares to {result}')

print('** 1. Create multiple processes **')
numbers = [1, 2, 3, 4]
start_time = time.time()
for number in numbers:
    process = Process(target=square, args=(number,))
    process.start()
process.join()

end_time = time.time()
print(f'Time difference  {end_time - start_time }')

#print('** 1. Create multiple processes **')

