import multiprocessing


print('*** Shared memory example for ctypes')

result =[ ]

def square_list(numlist, result, square_sum):
    for idx, num in enumerate(numlist):
        result[idx] = num * num
        square_sum.value = sum(result)

result = multiprocessing.Array('i', 4)
square_sum = multiprocessing.Value('i')

num_list = [1, 2, 3, 4]
p = multiprocessing.Process(target = square_list,
                            args = (num_list, result, square_sum))
p.start()
p.join()
print(list(result))

print('\n*** Shared memory example for non ctypes, using Manager class ***\n')

def get_data(data_list):
    for data in data_list:
        print("Name: %s \nScore: %d\n" % (data[0], data[1]))

def append_data(new_data, data_list):
    data_list.append(new_data)
    print("New data appended! \n")

with multiprocessing.Manager() as manager:
    database = (manager.list([('Maura', 70), ('Alexis', 79), ('Pete',96)]))
    new_data = ('Leroy', 87)
    p1 = multiprocessing.Process(target=append_data, args=(new_data, database))
    p2 = multiprocessing.Process(target=get_data, args=(database,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Data available to the Manager: ", database)

print('\n*** Multiprocess lock is similar to multithreading: \n'
        '\tlock.acquire, lock.release but from  multiprocessing module ***\n')

# Semaphors && events, conditions are similar  , queues:
# f.i.  q =  multiprocessing.Queue
# producer && consumer can be implemented with several processes
