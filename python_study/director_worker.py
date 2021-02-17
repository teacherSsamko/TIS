import asyncio
import time
import random

class Worker:
    def __init__(self, idx, task=10):
        self.idx = idx
        self.task = task
        self.isFinish = False
        self.work()
    
    def work(self):
        t = 0
        while t < self.task:
            t += 1
            print(f'{self.idx}...{t}/{self.task}')
            time.sleep(1)
        self.isFinish = True

class Director:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.task_to_do = list()
        self.workers = { x : None for x in range(4) }
        self.done_workers = set()

    def check_task(self, task):
        if task % 2 != 0:
            self.task_to_do.append(task)
            return self.task_to_do
        else:
            print(f'task empty...{task}')
            time.sleep(1)
            return False

    def check_avail_worker(self):
        for worker_idx, status in self.workers.items():
            if status == None:
                return worker_idx

        print('No avail worker')
        return False

    def assign_worker(self, worker_idx):
        worker = Worker(worker_idx, self.task_to_do.pop(0))
        self.workers[worker_idx] = worker

    def check_done_worker(self):
        for idx, worker in self.workers.items():
            if worker and worker.isFinish:
                print(f'worker {worker.idx} finished')
                self.workers[idx] = None


if __name__ == '__main__':
    tasks = random.sample(range(20), 10)
    print(tasks)
    director = Director()
    while tasks:
        if director.check_task(tasks.pop(0)):
            worker_idx = director.check_avail_worker()
            print(worker_idx)
            if worker_idx is not False:
                print('assign_worker')
                director.assign_worker(worker_idx)
        director.check_done_worker()



