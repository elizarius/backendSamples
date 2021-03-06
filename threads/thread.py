import threading
import time
from pprint import pprint

def threads_info():
    print(f'Number of threads: {threading.active_count()} \n')
    print(f'Threads enumerate: \n {threading.enumerate()} \n')

    print(f'Current thread: {threading.current_thread()} \n')

def demo_print():
    time.sleep(2)
    print(f'Demo thread:  {threading.current_thread().getName()} \n')

def calc_square(n):
    result = n * n
    print(f'The number {n} squares to {result}')


class DerivedThread(threading.Thread):

    def run(self):
        time.sleep(2)
        print(f'Hello from func called from th:  {threading.current_thread().getName()} \n')

amount = 0

def deposit(dep_amount, dep_lock):
    global amount
    for i in range(dep_amount):
        dep_lock.acquire()  #!!!
        amount += 1
        dep_lock.release()  #!!!

def two_deposit_threads(dep_amount):
    lock = threading.Lock()
    t1 = threading.Thread(target=deposit, args=(dep_amount, lock))
    t2 = threading.Thread(target=deposit, args=(dep_amount, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()



x= threading.Thread(name="AELZ_1", target = demo_print)

print(f'In thread: {threading.current_thread().getName()} \n')
x.start()
x.join()    # main thread waiting for return from children

print(f'Back to thread:  {threading.current_thread().getName()} \n')
#threads_info()

print(f'**** Running multiple  threads')

square_list = []
num_list = [1, 2, 3, 4]
for n in num_list:
    thread = threading.Thread(target=calc_square, args=(n, ))
    square_list.append(thread)
    thread.start()
    thread.join()


print(f'\n**** Running DERIVED THREAD INSTANCE')
obj = DerivedThread(name='Derived')
obj.start()
obj.join()  # run() starts automatically after.
print(f'Control returned to: {threading.current_thread().getName()}')

print(f'\n**** Threads Synchronization')
two_deposit_threads(10000)
print('Balance amount = {0}'.format(amount))


print(f'\n**** Releasing of double acquire')
lo = threading.Lock()
print ('First try :', lo.acquire())
print ('Second try:', lo.acquire(timeout=3)) #!!!

