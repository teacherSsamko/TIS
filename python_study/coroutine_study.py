import asyncio
import time

async def say_after(delay, what):
    print('before',what)
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(3, 'hello'))
    task2 = asyncio.create_task(say_after(1, 'world'))

    print(f'started at {time.strftime("%X")}')

    await task1
    await task2
    try:
        await asyncio.wait_for(say_after(10, 'world'), timeout=3.2) 
    except asyncio.TimeoutError:
        print('timeout!')

    print(f'finished at {time.strftime("%X")}')

asyncio.run(main())