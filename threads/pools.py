import os
import time
from multiprocessing import Pool

def cal_square(n):
    print(n, os.getpid())
    return n * n


print(f'cores: {os.cpu_count()}')

num_list = [1, 2, 3, 4, 5]
result = []

print(f'*** 1. Add tasks to  process pool, all cores ***')
p = Pool()
# map function is an analog of for loop
result = p.map(cal_square, num_list)
p.close()
p.join()

# pool distribute results between different processes
print (result)


print(f'\n\n*** 2. Add tasks to process pool, 2 cores ***')
p = Pool(processes=2)
# map function is an analog of for loop
result = p.map(cal_square, num_list)
p.close()
p.join()

# pool distribute results between different processes
print (result)

# See training on performance benchmarks examples when use and not pools 
# Process pools are extremally useful with several CPUs HW architecture
# ThreadPools  (futures) arew useful when IO tasks or long duration async tasks
