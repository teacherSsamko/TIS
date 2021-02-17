import asyncio
import time
import random
import threading

"""
python 3.5 +
"""
class Worker(threading.Thread):

    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        self.isFinish = False
        self.task = None
    
    def run(self):
        t = 0
        while t < self.task:
            t += 1
            print(f'{self.idx}...{t}/{self.task}')
            time.sleep(0.3)
        self.isFinish = True

class Director:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.task_to_do = list()
        self.workers = { x : None for x in range(capacity) }
        self.done_workers = set()

    def check_task(self, task):
        if task % 3 != 0:
            return True
        else:
            print(f'not to do...{task}')
            time.sleep(1)
            return False

    def check_avail_worker(self):
        for worker_idx, status in self.workers.items():
            if not status:
                return worker_idx
        print('No avail worker')
        time.sleep(1)
        return False

    def assign_worker(self, worker_idx, task):
        worker = Worker(worker_idx)
        worker.task = task
        self.workers[worker_idx] = worker
        worker.start()
        print(self.task_to_do)

    def check_done_worker(self):
        for idx, worker in self.workers.items():
            if worker and worker.isFinish:
                print(f'worker {worker.idx} finished')
                self.workers[idx] = None
                del worker

    async def work(self, tasks):
        self.task_to_do = tasks
        while self.task_to_do:
            task = self.task_to_do.pop(0)
            if self.check_task(task):
                while True:
                    worker_idx = self.check_avail_worker()
                    print(worker_idx)
                    if worker_idx is not False:
                        print(f'assign {task} to worker {worker_idx}')
                        self.assign_worker(worker_idx, task)
                        # async_task = self.assign_worker(worker_idx, task)
                        # await async_task
                        break                      
                self.check_done_worker()
                time.sleep(1)
                


async def main():
    tasks = random.sample(range(20), 10)
    print(tasks)
    director = Director(4)
    async_task1 = asyncio.create_task(director.work(tasks))
    print('task start')
    await async_task1

if __name__ == '__main__':
    # tasks = random.sample(range(20), 10)
    # print(tasks)
    # director = Director(3)
    # while tasks:
    #     if director.check_task(tasks.pop(0)):
    #         worker_idx = director.check_avail_worker()
    #         print(worker_idx)
    #         if worker_idx is not False:
    #             print(f'assign it to worker {worker_idx}')
                
    #     director.check_done_worker()
    try:
        asyncio.run(main())    
    except KeyboardInterrupt:
        print('forced finish')


