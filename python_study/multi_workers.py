import asyncio
import queue
import sys
import os
import threading
import subprocess
import datetime
import json
import time
import random


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Director:
    # director 
    """
    director만 반복하며 
    1) DB를 보고 taskQueue를 생성하고,
    2) workerList를 보고, gpu_avail할 때, worker생성
    3) timeout된 worker 강제 소멸
    4) gcs업로드(worker가 할 지 고민)
    """
    
    workers = []
    max_worker_count = os.cpu_count()*2-1

    def __init__(self, max_worker_count=None):
        """
        @type max_worker_count: int
        """
        if max_worker_count:
            self.max_worker_count = max_worker_count

    
    async def work(self):
        """
        반복해서 할 routine 작성
        """
        while True:
            if len(self.workers) < self.max_worker_count:
                task = asyncio.create_task(self.assign_worker())
            await asyncio.sleep(1)
            print('Current working workers => ', len(self.workers))
            task2 = asyncio.create_task(self.check_worker())

    async def assign_worker(self):
        print('assign worker')
        # assign worker here
        task= asyncio.create_task(self.assign_img_worker())
        await task
        print('worker assigned')
        # self.workers.append(worker)
    
    async def assign_img_worker(self):
        worker = ImgUpscaler()
        self.workers.append(worker)

    async def check_worker(self):
        print('check worker')
        poplist = []
        i = 0
        for worker in self.workers:
            if not worker.is_working:
                task = asyncio.create_task(worker.do_job()) # 이걸 task
                print(f'worker {worker.idx} start work')
            if worker.get_status():
                print(f'worker {worker.idx} out')
                del worker
                poplist.insert(0, i)
            i += 1
        for popindex in poplist:
            self.workers.pop(popindex)
        print('check worker finished')
        await asyncio.sleep(1)
            

class WorkerBase:
    """
    base class
    """
    worker_count = 0

    def __init__(self):
        # start_dt for checking timeout
        self.work_done = False
        self.is_working = False
        self.timelimit = datetime.timedelta(seconds=5)
        WorkerBase.worker_count += 1
        self.idx = WorkerBase.worker_count
        self.start_dt = datetime.datetime.now()
        print('worker init at', self.start_dt)
        # new task with start_dt

    def get_status(self):
        """
        director가 worker의 상태를 점검하는 method
        완료 혹은 timeout 판별 
        True: work is finished or timeout
        False: in Processing
        """
        if self.work_done:
            print(f'worker_{self.idx} => job finished')
            return True
        elif (datetime.datetime.now() - self.start_dt) < self.timelimit:
            return False
        else:
            print(f'worker_{self.idx} => timeout')
            self.work_done = True
            return True
    
    def set_timelimit(self, minutes):
        """
        @type minutes: int
        @param minutes: minutes
        """
        self.timelimit = datetime.timedelta(minutes=minutes)

    



class ImgUpscaler(WorkerBase):
    """
    Director로 부터 작업을 할당받아 
    업스케일링 진행
    """
    async def do_job(self):
        
        self.is_working = True
        i = 0
        size = random.randint(1, 100)
        print(f'{self.idx} job start >',size)
        while i < size and not self.work_done:
            # if i % 10 == 0:
            print(f'worker_{self.idx} => ',i)
            await asyncio.sleep(1)
            i += 1
        print('job done')
        self.work_done = True


    

class VidUpscaler(WorkerBase):
    """
    Director로 부터 queue에 있는 Video 작업을 할당받아 
    업스케일링 진행
    """
    
    


async def main():
    director = Director()
    lcpu = os.cpu_count()*2-1
    print('CPU=>',lcpu)
    
    task1 = asyncio.create_task(director.work())

    await task1
    
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('finish')