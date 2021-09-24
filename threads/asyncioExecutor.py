import asyncio
import time

async def zz():
    print ('Hello')

async def main():
    start = time.time()

    #await greetings('Hello')
    #await greetings('World')

    task1 = asyncio.create_task(greetings('Hello'))
    task2 = asyncio.create_task(greetings('World'))

    await task1
    await task2

    print('Control returned to main')
    print('Total time taken:', time.time() - start)

    print ('\n*** 3.  Asyncio GATHER example')
    start = time.time()
    await asyncio.gather(greetings('Hello'),
                         greetings('WO'),
                         print_numbers(6))

    print('Total time for GATHER taken:', time.time() - start)


async def greetings(msg):
    for i in range(6):
        print(msg)
        await asyncio.sleep(1)


async def print_numbers(num):
    for i in range(num):
        print(i)
        await asyncio.sleep(1)



func = zz()
print (type(func))

print ('*** 1.  Asyncio example')
loop = asyncio.get_event_loop()
loop.run_until_complete(zz())
loop.run_until_complete(func)
loop.close()

print ('\n*** 2.  Asyncio example')
asyncio.run(main())
