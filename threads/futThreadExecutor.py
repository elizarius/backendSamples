import os
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, get_ident

num_list = [1, 2, 3, 4, 5]


def return_after_n_secs(n, message):
    time.sleep(n)
    return message

def cal_square(n):
    print(n, get_ident())
    return n * n

def executor_func():
    with ThreadPoolExecutor(max_workers = 3) as executor:
        results = executor.map(cal_square, num_list)
    return results


print(f'*** 1. Add tasks to  thread executor pool,  LONG RUNNING TASKS ***')
pool = ThreadPoolExecutor(3)

# submit for individual task
submitted_job = pool.submit(return_after_n_secs, 10, 'Hello')
print('Task done? :', submitted_job.done())
# Wait until done, blocking call
print(submitted_job.result())
print('Task done? :', submitted_job.done())

# map used for multiple tasks
print(f'\n\n*** 2.  Using executor function ***')
square_data = executor_func()
print(list(square_data))
   
# Process pools are extremally useful with several CPUs HW architecture
# ThreadPools  (futures) are useful when IO tasks or long running async tasks
