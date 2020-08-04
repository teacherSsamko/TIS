from threading import Thread
import time

def my_thread(val):
    for i in range(val):
        print(f'my_thread({i}')
        print('is my t1 alive? ',t1.is_alive())
        time.sleep(1)

t1 = Thread(target=my_thread, args=(5, ))

t1.start()
t1.join(timeout=3)

# main
for i in range(3):
    print(f"it's main process ({i})")
    print('is t1 alive? ',t1.is_alive())
    time.sleep(1)

print('---end---')
