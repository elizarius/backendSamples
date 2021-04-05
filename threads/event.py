import threading
import time
from pprint import pprint
import random

# Event: to communicate between threads
event = threading.Event()
print(dir(event))

meeting = threading.Event()
def hold_meeting():
    meeting.set()
    print('Event is set. The meeting has begun')
    time.sleep(6)
    print('The meeting is complete. Clearing the event...')
    meeting.clear()

def enter_conference_room():
    time.sleep(1)
    meeting.wait()

    while meeting.is_set():
        print("Waiting for the meeting to end")
        time.sleep(0.5)
    print("The meeting is done. Entering the conference room...")


def produce():
    global container
    global counter
    global more_to_come

    for i in range(5):
        time.sleep(random.randrange(2, 5))

        condition.acquire()
        item = "News item #" + str(counter)
        container.append(item)
        counter +=1
        print("\nProduced:", item)
        condition.notify_all()
        condition.release()
    more_to_come = False

def consume():
    global more_to_come
    while(more_to_come):
        condition.acquire()
        condition.wait()

        time.sleep(random.random())
        print(threading.current_thread().getName(),  "acquired:" , container[-1])
        condition.release()


print(f'\n**** Event Object example')
t1 = threading.Thread(target = hold_meeting)
t2 = threading.Thread(target = enter_conference_room)
t1.start()
t2.start()
t1.join()
t2.join()

print(f'\n**** Condition Object example')
condition = threading.Condition()
container = []
counter = 1
more_to_come = True

producer_thread = threading.Thread(target=produce)
consumer_one_thread = threading.Thread(target=consume, 
                                        name="News Site One",)
consumer_two_thread = threading.Thread(target=consume,
                                        name="News Site Two")
consumer_three_thread = threading.Thread(target=consume,
                                        name="News Site Three")
   
threads = [ producer_thread,
            consumer_one_thread,
            consumer_two_thread,
            consumer_three_thread
            ]

for t in threads:
    t.start()

for t in threads:
    t.join()

time.sleep(1)
print("\nAll done")

