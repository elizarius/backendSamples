import threading
import time
from pprint import pprint


data_one = 3
data_two = 5
lock_one = threading.Lock()
lock_two = threading.Lock()


def my_process(lock_one, lock_two):
    global data_one
    global data_two

    lock_one.acquire()
    print(threading.current_thread().name, " incrementing data_one")
    data_one += 1
    time.sleep(1)

    lock_two.acquire()
    print(threading.current_thread().name, " incrementing data_two")
    data_two += 1
    time.sleep(1)

    lock_one.release()
    lock_two.release()
 

# Eliminate of deadlocks: release lock immediately after usage
def my_process_1(lock_one, lock_two):
    global data_one
    global data_two

    lock_one.acquire()
    print(threading.current_thread().name, " incrementing data_one")
    data_one += 1
    time.sleep(1)
    lock_one.release()

    lock_two.acquire()
    print(threading.current_thread().name, " incrementing data_two")
    data_two += 1
    time.sleep(1)
    lock_two.release()


# Sync by semaphores: oldest mechanizm
def sem_func():
    semaphore.acquire()
    time.sleep(0.1)
    print(threading.current_thread().name,  " acquired the semaphore")
    print("Semaphore value after acquire:", semaphore._value)
    time.sleep(5)
    semaphore.release()
    print("Semaphore value after release:", semaphore._value)




def place_order():
    print ("Order placed")
    semaphore.acquire()
    print ("Customer order number is:", order_num)

def prepare_order():
    global order_num
    time.sleep(3)
    order_num += 1
    print ("Preparing order number", order_num)
    semaphore.release()


print('***  Swap T2 arguments to simulate deadlock' )
t1 = threading.Thread(target=my_process, args=(lock_one, lock_two))
t2 = threading.Thread(target=my_process, args=(lock_one, lock_two))
t1.start()
t2.start()
t1.join()
t2.join()
   
print("data_one:", data_one)
print("data_two:", data_two)


print('\n***  Be sure that deadlock eliminated' )
t1 = threading.Thread(target=my_process_1, args=(lock_one, lock_two))
t2 = threading.Thread(target=my_process_1, args=(lock_two, lock_two))
t1.start()
t2.start()
t1.join()
t2.join()
   
print("data_one:", data_one)
print("data_two:", data_two)

print('\n***  Semaphores sync demo' )
semaphore = threading.Semaphore(value=3)
t1 = threading.Thread(target=sem_func)
t2 = threading.Thread(target=sem_func)
print("Initial Semaphore value: ", semaphore._value)
start_time = time.time()
t1.start()
t2.start()

t1.join()
t2.join()
end_time = time.time()
print("Total time: ", end_time-start_time)


print('\n***  Semaphores sync: release called from different thread, contrary lock' )
order_num = 0
semaphore = threading.Semaphore(0)
for i in range (0, 4):
    t1 = threading.Thread(target=place_order)
    t2 = threading.Thread(target=prepare_order)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

print('\n***  Semaphores release usage: --> as producer - consumer' )
semaphore = threading.Semaphore()
semaphore.release()
semaphore.release()
semaphore.release()
print('***  Semaphore value {}'.format(semaphore._value))

# BoundedSemaphore provides a bounded counter, which raises an error 
# if a release() call tries to increase the counter beyond its maximum size
semaphore = threading.BoundedSemaphore(2)
print('\n*** Bounded  Semaphore value {}'.format(semaphore._value))
semaphore.acquire()
semaphore.release()
#semaphore.release()
#semaphore.release()
print('*** Bounded  Semaphore value after release(s) {}'.format(semaphore._value))

