import asyncio
import time

@asyncio.coroutine
def eternity():
    time.sleep(3600)
    print('yay!')

@asyncio.coroutine
def main():
    pass


loop = asyncio.get_event_loop()

loop.create_task(eternity())

try:
    loop.run_forever()
except:
    loop.close()