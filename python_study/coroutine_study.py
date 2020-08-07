import asyncio
import time

async def say_after(delay, what):
    print('before',what)
    await asyncio.sleep(delay)
    print(what)

async def count_up(count):
    for i in range(count):
        print(i+1)
        await asyncio.sleep(0.7)

async def main():
    task1 = asyncio.create_task(say_after(3, 'hello'))
    task3 = asyncio.create_task(count_up(10))
    task2 = asyncio.create_task(say_after(1, 'world'))
    task4 = asyncio.create_task(count_up(4))

    print(f'started at {time.strftime("%X")}')

    await task1
    await task2
    try:
        await asyncio.wait_for(say_after(10, 'world'), timeout=3.2) 
    except asyncio.TimeoutError:
        print('timeout!')

    print(f'finished at {time.strftime("%X")}')

asyncio.run(main())