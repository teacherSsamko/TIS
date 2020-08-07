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
from multiprocessing import Queue, Process



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
    tasks_that_are_done = Queue()
    tasks_to_accomplish = Queue()
    accomplish_set = set()
    done_set = set()
    workers = []


    def __init__(self):
        pass
    
    async def work(self):
        while True:
            if len(self.workers) < 4:
                task = asyncio.create_task(self.assign_worker())
            await asyncio.sleep(1)
            print('len of workers => ', len(self.workers))
            task2 = asyncio.create_task(self.check_worker())

    async def assign_worker(self):
        print('assign worker')
        condition = random.randint(1,2)
        if condition != 1:
            print('condition =>', condition)
            print('sleep 1 sec')
            await asyncio.sleep(1)
        else:
            # assign worker here
            # worker = asyncio.ensure_future(self.assign_img_worker())
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
            if worker.get_status():
                print(f'worker {i} out')
                poplist.insert(0, i)
            i += 1
        for popindex in poplist:
            self.workers.pop(popindex)
        print('check worker finished')
        await asyncio.sleep(1)
            

class UpscalerBase:
    """
    base class
    """
    work_done = False
    is_working = False
    timelimit = datetime.timedelta(seconds=5)

    async def __aenter__(self):
        print('async enter')

    async def __aexit__(self, exc_type, exc_value, traceback):
        print('async exit')

    def __init__(self):
        # start_dt for checking timeout
        self.start_dt = datetime.datetime.now()
        print('worker init at', self.start_dt)
        # new task with start_dt

    def get_status(self):
            """
            director가 worker의 상태를 점검하는 method
            완료 혹은 timeout 판별 
            True: work is finished whatever it upscaled well or not
            False: in Processing
            """
            if self.work_done:
                return True
            elif (datetime.datetime.now() - self.start_dt) < self.timelimit:
                return False
            else:
                return True
    
    def set_timelimit(self, minutes):
        """
        @type minutes: int
        @param minutes: minutes
        """
        self.timelimit = datetime.timedelta(minutes=minutes)

    



class ImgUpscaler(UpscalerBase):
    """
    Director로 부터 queue에 있는 Image 작업을 할당받아 
    업스케일링 진행
    """
    def __init__(self):
        super().__init__()

    async def do_job(self):
        i = 0
        size = random.randint(1, 10)
        print('job start >',size)
        while i < size:
            print(i)
            await asyncio.sleep(1)
            i += 1
        print('job done')


    

class VidUpscaler(UpscalerBase):
    """
    Director로 부터 queue에 있는 Video 작업을 할당받아 
    업스케일링 진행
    """
    def __init__(self, task, gpu_avail):
        super().__init__(task, gpu_avail)
    


"""
4개의 프로세스가 동시에 작동하도록
Director
Worker * 3
"""

director = Director()

lcpu = os.cpu_count()*2-1
async def main():
    print('CPU=>',lcpu)
    task1 = asyncio.create_task(director.work())

    await task1
    print('finish')

asyncio.run(main())