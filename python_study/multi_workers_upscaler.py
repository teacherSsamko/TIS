#!/root/.pyenv/versions/3.7.3/bin/python
import asyncio
import queue
import sys
import os
import threading
import subprocess
import signal
import datetime
import json
import time
import datetime
import requests
import smtplib
import logging
from multiprocessing import Queue
from email.mime.text import MIMEText

import GPUtil
import socketio
import redis
from google.cloud import storage

import dbConn as dbConn_video
import dbConn_img 
from config.config import config_by_name
from redis_helper import RedisClient
from helpers.mail_helper import send_mail, send_success_mail, send_fail_mail
from helpers.gcs_helper import failed_file_move, upload_to_gcs

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/mnt/gdf/ff_server/config/gdf-service-5ba9c3b0b7a5.json"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'data/out/')
SRLOG_DIR = os.path.join(BASE_DIR, 'srlog')
AIMODEL_PATH = '/mnt/gdf/ff_server/pb/'
gpuscript = '/usr/local/bin/ff_gpu0'
config = config_by_name[os.getenv('ENV')]

# socket io connection
server = os.environ['ENV']
socketio_url = config.SOCKET_IO_URL
sio = socketio.Client()
sio.connect(socketio_url)

# r = RedisClient()
pikavue = config.SMTP

# smtp client
smtp = smtplib.SMTP(host=pikavue['host'], port=pikavue['port'])
smtp.starttls()
smtp.ehlo()
smtp.login(pikavue['auth']['user'],pikavue['auth']['pass'])

# logging
logfile = config.LOGGING['log_dir']+'upscale.log'
logging.basicConfig(filename=logfile, level=logging.INFO)


class Director:
    """
    director만 반복하며 
    1) DB를 보고 taskQueue를 생성하고,
    2) workerList를 보고, gpu_avail할 때, worker생성
    3) timeout된 worker 강제 소멸
    4) gcs업로드(worker가 할 지 고민)
    """
    accomplish_set = set()
    done_set = set()
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    workers = []
    max_worker_count = os.cpu_count()*2-1

    def __init__(self, max_worker_count=None):
        """
        @type max_worker_count: int
        """
        if max_worker_count:
            self.max_worker_count = max_worker_count

        # smtp client
        self.pikavue = config.SMTP
        self.smtp = smtplib.SMTP(host=self.pikavue['host'], port=self.pikavue['port'])
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(self.pikavue['auth']['user'],self.pikavue['auth']['pass'])

    def pre_work(self):
        """
        시작전에 불완전 종료된 데이터에 대한 처리. 
        queue에 들어갔던 데이터들 다시 대기상태로
        """
        cursor_img = dbConn_img.DBConn.getCursor()
        cursor_video = dbConn_video.DBConn.getCursor()
        inQueue_imgs = dbConn_img.DBConn.get_image_inQueueStatus()
        inQueue_videos = dbConn_video.DBConn.get_video_inQueueStatus()

        stopped_imgs = dbConn_img.DBConn.get_image_RunningStatus()
        stopped_videos = dbConn_video.DBConn.get_video_RunningStatus()


        if len(inQueue_imgs) > 0:
            for img in inQueue_imgs:
                dbConn_img.DBConn.set_image_WaitStatus(img[0])
        if len(inQueue_videos) > 0:
            for video in inQueue_videos:
                dbConn_video.DBConn.set_video_WaitStatus(video[0])
                logging.info(f"wait status {video[0]}")

        if len(stopped_imgs) > 0:
            for img in stopped_imgs:
                dbConn_img.DBConn.set_image_TimeoutStatus(img[0])
                refund_url = config.REFUND_API_URL
                data = {
                    'uid':img[1],
                    'idx':img[0],
                    'isImage':'true'
                }
                res = requests.post(url=refund_url, data=data)
        if len(stopped_videos) > 0:
            for video in stopped_videos:
                dbConn_video.DBConn.set_video_TimeoutStatus(video[0])
                refund_url = config.REFUND_API_URL
                logging.info(video[0])
                data = {
                    'uid':video[1],
                    'idx':video[0],
                    'isImage':'false'
                }
                res = requests.post(url=refund_url, data=data)

        logging.info("prework finished well")



    async def work(self):
        """
        반복해서 할 routine 작성
        """
        while True:
            # DB check
            self.check_imageDB()
            self.check_videoDB()
            # gpu avail check
            # print('Current working workers => ', len(self.workers))
            async_task2 = asyncio.create_task(self.check_worker())
            self.after_process()
            gpu_id = self.get_available_device() 
            # print('gpu_id =>',gpu_id)
            if gpu_id == -1:
                await asyncio.sleep(1)
                continue
            if len(self.workers) < self.max_worker_count and not self.tasks_to_accomplish.empty():
                # get from queue
                print("director will assign job to worker") 
                job = self.tasks_to_accomplish.get_nowait()
                print("job => ", job) 
                logging.info("job => %s", job)
                async_task = asyncio.create_task(self.assign_worker(job, gpu_id))
                time.sleep(7)
                await asyncio.sleep(5)
                print('assigned worker => ', async_task)
                logging.info('assigned worker => %s', async_task)
            await asyncio.sleep(1)
            # upload to gcs


    async def assign_worker(self, job, gpu_id):
        print('assign worker')
        # assign worker here
        isImage = job[-1]
        if isImage:
            print('assign image worker')
            logging.info('assign image worker')
            async_task= asyncio.create_task(self.assign_img_worker(job, gpu_id))
        else:
            print('assign video worker')
            logging.info('assign video worker')
            async_task= asyncio.create_task(self.assign_vid_worker(job, gpu_id))

        await async_task
        
        # print('worker assigned')
        # self.workers.append(worker)
    
    async def assign_img_worker(self, job, gpu_id):
        print('assign imageworker(job, gpu) =>', job, gpu_id)
        worker = ImgUpscaler(job, gpu_id)
        print('worker => ', worker)
        logging.info('image worker => %s', worker)
        self.workers.append(worker)
        print("img worker assigned")
        logging.info("img worker assigned")
    
    async def assign_vid_worker(self, job, gpu_id):
        print('assign videoworker(job, gpu) =>', job, gpu_id)
        worker = VidUpscaler(job, gpu_id)
        print('worker => ', worker)
        logging.info('video worker => %s', worker)
        self.workers.append(worker)
        print("video worker assigned")
        logging.info("video worker assigned")

    async def check_worker(self):
        # print('check worker')
        poplist = []
        i = 0
        for worker in self.workers:
            if not worker.is_working:
                async_task = asyncio.create_task(worker.do_job()) # 이걸 task
                print(f'worker {worker.idx} start work')
                logging.info(f'worker {worker.idx} start work')
            if worker.get_status():
                self.accomplish_set.remove(worker.origin_task)
                self.done_set.add(worker.completed_task)
                self.tasks_that_are_done.put(worker.completed_task)
                print(f'worker {worker.idx} out')
                logging.info(f'worker {worker.idx} out')
                del worker
                poplist.insert(0, i)
            i += 1
        for popindex in poplist:
            self.workers.pop(popindex)
        # print('check worker finished')
        
        await asyncio.sleep(1)

    def get_available_device(max_memory=0.49):
        GPUs = GPUtil.getGPUs()
        # print('GPUs =>',GPUs)
        # try:
        #     p = subprocess.Popen(["/usr/bin/nvidia-smi","--query-gpu=index,memory.total","--format=csv,noheader,nounits"], stdout=subprocess.PIPE)
        #     stdout = p.communicate()
        #     print('stdout =>',stdout)
        #     output = stdout[0].decode("UTF-8")
        #     print('output =>',output)
        #     lines = output.split(os.linesep)
        #     print('lines =>',lines)
        # except Exception as e:
        #     print('Popen error')
        #     print(e)
        freeMemory = 0
        available = -1
        max_memory = 0.64
        for GPU in GPUs:
            # print('GPU memory util =>', GPU.memoryUtil)
            # print('GPU memory free =>', GPU.memoryFree)
            # print('GPU.memoryUtil type =>', type(GPU.memoryUtil))
            # print('max_memory type =>', type(max_memory))
            if GPU.memoryUtil > max_memory:
                continue
            if GPU.memoryFree >= freeMemory:
                freeMemory = GPU.memoryFree
                available = GPU.id
        # print('avail =>',available)
        return available

    def check_imageDB(self):
        # print('check image DB')
        cursor = dbConn_img.DBConn.getCursor()
        tasks = dbConn_img.DBConn.get_image_WaitStatus()
        # @type tasks: tuple
        number_of_task = len(tasks)
        if number_of_task > 0:
            print("tasks count:",number_of_task)
            logging.info("tasks count: %s",number_of_task)
            for i in range(number_of_task):
                # tasks[i] = (idx,hashkey,origin_file_name,model,user_id,brightness,saturation,hue,sharpen)
                img_task = (*tasks[i], True) # isImage = True
                print("step1 task[{0}]={1}".format(i,tasks[i]))
                logging.info("step1 task[{0}]={1}".format(i,tasks[i]))
                if img_task not in self.accomplish_set:
                    cursor = dbConn_img.DBConn.getCursor()
                    dbConn_img.DBConn.set_image_WaitingStatus(img_task[0])
                    self.accomplish_set.add(img_task)
                    print('accomplish set =>', self.accomplish_set)
                    logging.info('accomplish set => %s', self.accomplish_set)
                    self.tasks_to_accomplish.put(img_task)   
                    print('tasks to accomplisth =>', self.tasks_to_accomplish)
                    logging.info('tasks to accomplisth => %s', self.tasks_to_accomplish)
                else:
                    print('this task is already in accomplish_set =>', img_task)
                    logging.info('this task is already in accomplish_set => %s', img_task)
            
    def check_videoDB(self):
        # print('check video DB')
        cursor = dbConn_video.DBConn.getCursor()
        tasks = dbConn_video.DBConn.get_video_WaitStatus()
        number_of_task = len(tasks)
        if number_of_task > 0:
            print("tasks:",number_of_task)
            for i in range(number_of_task):
                # tasks[i] = (id, origin_path, model, uid)
                video_task = (*tasks[i], False)
                print("step1 task[{0}]={1}".format(i,tasks[i]))
                logging.info("step1 task[{0}]={1}".format(i,tasks[i]))
                if video_task not in self.accomplish_set:
                    cursor = dbConn_video.DBConn.getCursor()
                    dbConn_video.DBConn.set_video_WaitingStatus(video_task[0])
                    self.accomplish_set.add(video_task)
                    print('accomplish set =>', self.accomplish_set)
                    logging.info('accomplish set => %s', self.accomplish_set)
                    self.tasks_to_accomplish.put(video_task)   
                    print('tasks to accomplisth =>', self.tasks_to_accomplish)
                    logging.info('tasks to accomplisth => %s', self.tasks_to_accomplish)
                else:
                    print('this task is already in accomplish_set =>', self.accomplish_set)
                    logging.info('this task is already in accomplish_set => %s', self.accomplish_set)
            
    def after_process(self):
        while not self.tasks_that_are_done.empty():
            completed_task = self.tasks_that_are_done.get()
            self.done_set.remove(completed_task)
            # (132, 'upload/small_pKzorSy.mp4', '1x2_3c', datetime.datetime(2020, 6, 3, 3, 19, 39, 562240), 'Process-2')
            # update complete time and processing time 
            # completed_task[-1] : 'isImage' argument
            isNotTimeout = completed_task[-1]
            print('is timed out?',isNotTimeout)
            logging.info('is timed out? %s',isNotTimeout)
            isImage = completed_task[-3]
            print('is Image?',isImage)
            logging.info('is Image? %s',isImage)
            if isImage:
                self.image_after_proc(completed_task)
            else:
                self.video_after_proc(completed_task)

    def upload_upscaled_to_gcs(self, isImage, upscaled_file_path, origin_file_name):
        print('upload image?',isImage)
        logging.info('upload image? %s',isImage)
        return upload_to_gcs(isImage, upscaled_file_path, origin_file_name)
    
    def image_after_proc(self, completed_task):
        if completed_task[-1]:
            filename = completed_task[1] + '.' + completed_task[2].split(".")[-1]
            print('MEDIA_ROOT+filename',MEDIA_ROOT+filename)
            origin_file_name = completed_task[2]
            isImage = completed_task[-3]
            newfile = self.upload_upscaled_to_gcs(isImage ,MEDIA_ROOT+filename, origin_file_name)
            cursor = dbConn_img.DBConn.getCursor()
            dbConn_img.DBConn.set_image_CompleteStatus(completed_task[0],completed_task[4],newfile)
            # r.update_progress(completed_task[1],95,True)
            sio.emit('send_event', {'event': 'image_progress_update','userId': completed_task[4],'idx': completed_task[0],'progress': 95 })
            # redisProgressUpdate(userReqInfo.hashKeyName, 10, true)
            print("step4 completed_task:id={0},upscaled file={1}".format(completed_task[0],newfile))
            logging.info("step4 completed_task:id={0},upscaled file={1}".format(completed_task[0],newfile))
            sio.emit('send_event', { 'event': 'image_completed_upscaling','userId': completed_task[4],'idx': completed_task[0], 'downloadUrl': newfile })
            mail_body = f'upscaled image path = {newfile}'
            self.send_mail(body=mail_body, subject='image upscaled')
            send_success_mail(completed_task[4])
            logging.info('image ok mail sent')
        else:
            print("step4 failed_task:id={}".format(completed_task[0]))
            logging.info("step4 failed_task:id={}".format(completed_task[0]))
            sio.emit('send_event', {'event': 'image_progress_fail','userId': completed_task[4],'idx': completed_task[0]})
            dbConn_img.DBConn.set_image_TimeoutStatus(completed_task[0])
            # refund api 
            refund_url = config.REFUND_API_URL
            data = {
                'uid':completed_task[4],
                'idx':completed_task[0],
                'isImage':'true'
            }
            res = requests.post(url=refund_url, data=data)
            print(res)
            logging.info(res)
            print(f'task({completed_task[0]}) failed')
            logging.info(f'task({completed_task[0]}) failed')
            # origin_file_path_prefix = 'https://storage.googleapis.com/gdf-web-storage/image/origin/'
            origin_file_path_prefix = 'image/origin/'
            hashkey = completed_task[1]
            file_ext = completed_task[2].split(".")[-1]
            origin_file_path = f'{origin_file_path_prefix+hashkey}.{file_ext}'
            moved_path = failed_file_move(True, origin_file_path)
            mail_body = f'failed upscale image origin path = {moved_path}'
            self.send_mail(body=mail_body, subject='image upscale failed')
            send_fail_mail(completed_task[4])
            logging.info('image fail mail sent')

    def video_after_proc(self, completed_task):
        if completed_task[-1]:
            hashed_file_name = completed_task[1].split('/')[-1]
            print('MEDIA_ROOT+hashed_file_name',MEDIA_ROOT+hashed_file_name)
            isImage = completed_task[-3]
            origin_file_name = completed_task[4]
            upscaled_file_name = origin_file_name.split(".")[0]+".mp4"
            newfile = self.upload_upscaled_to_gcs(isImage, MEDIA_ROOT+hashed_file_name, upscaled_file_name)
            cursor = dbConn_video.DBConn.getCursor()
            print('completed_task',completed_task)
            logging.info('completed_task %s',completed_task)
            dbConn_video.DBConn.set_video_CompleteStatus(completed_task[0],completed_task[-1],newfile)
            hashkey = hashed_file_name.split(".")[0]
            # r.update_progress(hashkey,95,True)
            sio.emit('send_event', {'event': 'video_progress_update','userId': completed_task[3],'idx': completed_task[0],'progress': 95 })
            print("step4 completed_task:id={0},upscaled file={1}".format(completed_task[0],newfile))
            logging.info("step4 completed_task:id={0},upscaled file={1}".format(completed_task[0],newfile))
            sio.emit('send_event', { 'event': 'video_completed_upscaling','userId': completed_task[3],'idx': completed_task[0], 'downloadUrl': newfile })
            mail_body = f'upscaled video path = {newfile}'
            self.send_mail(body=mail_body, subject='video upscaled')
            send_success_mail(completed_task[3])
            logging.info('video ok mail sent')
        else:
            print("step4 failed_task:id={}".format(completed_task[0]))
            logging.info("step4 failed_task:id={}".format(completed_task[0]))
            dbConn_video.DBConn.set_video_TimeoutStatus(completed_task[0])
            # refund api 
            refund_url = config.REFUND_API_URL
            data = {
                'uid':completed_task[3],
                'idx':completed_task[0],
                'isImage':'false'
            }
            res = requests.post(url=refund_url, data=data)
            logging.info('refund ok')
            sio.emit('send_event', {'event': 'video_progress_fail','userId': completed_task[3],'idx': completed_task[0]})
            try:
                print(res.text)
                logging.info(res.text)
            except:
                print('res=>',res)
                logging.info('res=> %s',res)
            print(f'task({completed_task[0]}) failed')
            logging.info(f'task({completed_task[0]}) failed')
            origin_file_path = completed_task[1].split("/")[4:]
            origin_file_path = "/".join(origin_file_path)
            logging.info(f"origin file path => {origin_file_path}")
            moved_path = failed_file_move(False, origin_file_path)
            # moved_path = failed_file_move(False, completed_task[1])
            mail_body = f'failed upscale video origin path = {moved_path}'
            # mail_body = f'failed upscale video origin path = {completed_task[1]}'
            self.send_mail(body=mail_body, subject='video upscale failed')
            send_fail_mail(completed_task[3])
            logging.info('video fail mail sent')

    def send_mail(self, body, subject='Test', to='ssamko@gdflab.com'):
        # smtp client
        self.pikavue = config.SMTP
        self.smtp = smtplib.SMTP(host=self.pikavue['host'], port=self.pikavue['port'])
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(self.pikavue['auth']['user'],self.pikavue['auth']['pass'])
        try:
            msg = MIMEText(body)
            from_addr = self.pikavue['auth']['user']
            msg['Subject'] = subject
            msg['To'] = to
            msg['From'] = from_addr
            self.smtp.sendmail(from_addr=from_addr, to_addrs=to, msg=msg.as_string())
            print("mail sent")
            self.smtp.quit()
            return True
        except Exception as e:
            print("mail fail =>",e)
            logging.warning(f'mail fail => {e}')
            return False

class Worker:
    """
    base class
    """
    worker_count = 0

    def __init__(self, task, gpu_avail):
        print('workerbase init')
        self.work_done = False
        self.is_working = False
        # set timelimit
        self.timelimit = config.TIMEOUT
        Worker.worker_count += 1
        self.idx = Worker.worker_count
        self.start_dt = datetime.datetime.now()
        print('worker init at', self.start_dt)
        logging.info('worker init at %s', self.start_dt)
        self.task = (*task, self.start_dt)
        self.origin_task = task
        self.gpu_avail = gpu_avail

    def get_status(self):
        """
        director가 worker의 상태를 점검하는 method
        완료 혹은 timeout 판별 
        True: work is finished or timeout
        False: in Processing
        """
        if self.work_done:
            print(f'worker_{self.idx} => job finished')
            logging.info(f'worker_{self.idx} => job finished')
            return True
        elif (datetime.datetime.now() - self.start_dt) < self.timelimit:
            return False
        else:
            print(f'worker_{self.idx} => timeout')
            logging.info(f'worker_{self.idx} => timeout')
            print(f'proc pid => {self.proc.pid}')
            logging.info(f'proc pid => {self.proc.pid}')
            self.completed_task = (*self.task, False)
            # self.proc.terminate()
            # self.proc.kill()
            os.killpg(os.getpgid(self.proc.pid + 1), signal.SIGTERM)
            os.system(f"/bin/kill -9 {self.proc.pid + 1}")
            print('worker killed')
            logging.info('worker killed')
            self.work_done = True
            return True
    
    def set_timelimit(self, minutes):
        """
        @type minutes: int
        @param minutes: minutes
        """
        self.timelimit = datetime.timedelta(minutes=minutes)

class ImgUpscaler(Worker):

    gcs_origin_path_prefix = 'https://storage.googleapis.com/gdf-web-storage/image/origin/'

    def __init__(self, task, gpu_avail):
        print('imgupscaler init')
        logging.info('imgupscaler init')
        super().__init__(task, gpu_avail)
        self.id = task[0]
        file_ext = task[2].split(".")[-1]
        self.hashkey = task[1]
        # FO76 Original Map.jpeg
        self.origin_file_name = task[2]
        self.hashed_file_name = self.hashkey+'.'+file_ext
        # vename, image_fullpath -> origin_file_path
        self.origin_file_path = self.gcs_origin_path_prefix+self.hashed_file_name
        self.aimodel_name = task[3]
        self.brightness = task[5]
        self.saturation = task[6]
        self.hue = task[7]
        self.sharpen = self.sharpen_model(task[8])
        self.sr_output_file_name = self.origin_file_path.split('/')[-1]
        self.sr_image_fullpath = MEDIA_ROOT + self.sr_output_file_name
        self.aimodel_path = AIMODEL_PATH + self.aimodel_name +'_3c.pb' 

    async def do_job(self):
        self.is_working = True
        print(f'{self.idx} job start ')
        logging.info(f'{self.idx} job start ')
        self.get_file_info()
        result= asyncio.create_task(self.do_upscale())
        print('job done. work result=', result)
        logging.info('job done. work result= %s', result)
        await asyncio.sleep(1)
        # self.work_done = True

    def get_file_info(self):
        # 파일 정보가져오기
        print(f'worker {self.idx} get file_info')
        sio.emit('send_event', {"event": "image_start_image_upscaling","userId": self.task[4],'idx': self.task[0] })
        batcmd = F"""/usr/local/bin/ffprobe -v quiet -print_format json -show_format -show_streams -select_streams v:0 {self.origin_file_path}"""
        self.result = json.loads(subprocess.check_output(batcmd, shell=True))
        self.codec = self.result["streams"][0]["codec_tag_string"].lower()  
        self.cursor = dbConn_img.DBConn.getCursor() # 이건 왜?
        dbConn_img.DBConn.set_image_RunningStatus(self.id, self.sr_output_file_name) 
        print('codec=>',self.codec)

    async def do_upscale(self):
        print("start to upscale")
        logging.info("start to upscale")
        self.is_working = True
        cmd = F"""FFREPORT=file={SRLOG_DIR}/{self.id}_{self.sr_output_file_name}.report:level=32 {gpuscript} -progress pipe:1 -y -i {self.origin_file_path} -vf "eq=contrast=1,sr=dnn_backend=tensorflow:model={self.aimodel_path}:gpu_index={self.gpu_avail},hue=h={self.hue}:s={self.saturation}:b={self.brightness},convolution={self.sharpen}" {self.sr_image_fullpath} tile_size=300"""
        print(cmd)
        logging.info(cmd)
        self.proc = await asyncio.create_subprocess_shell(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE ,encoding='utf-8', bufsize=0,shell=True, universal_newlines=False )
        # self.proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE ,encoding='utf-8', bufsize=0,shell=True)
        try:
            print("step2 - started upscaling id=", self.task[0], f'-- [{datetime.datetime.now()}]')
            logging.info(f"step2 - started upscaling id={self.task[0]} -- [{datetime.datetime.now()}]")
            # r.update_progress(completed_task[1],10,True)
            sio.emit('send_event', {'event': 'image_progress_update','userId': self.task[4],'idx': self.task[0],'progress': 10 })
            ret = await self.proc.wait()
            # ret = await asyncio.wait_for(self.proc, 70.0)

        except:
            print("upscale fail")
            logging.warning("upscale fail")
        finally:
            try:
                print("step3 - ended upscaling,id={0},rc={1}".format(self.task[0],self.proc.returncode))
                logging.info("step3 - ended upscaling,id={0},rc={1}".format(self.task[0],self.proc.returncode))
                if self.proc.returncode==0:
                    sio.emit('send_event', {'event': 'image_progress_update','userId': self.task[4],'idx': self.task[0],'progress': 90 })
                    complete_dt = datetime.datetime.now()
                    self.completed_task = (*self.task, complete_dt) #OK
                    print('completed_task=>', self.completed_task)
                    logging.info('completed_task=> %s', self.completed_task)
                    self.work_done = True
                    return True
                # returncode가 0이 아니면 error처리
                else:
                    sio.emit('send_event', {'event': 'image_progress_fail','userId': self.task[4],'idx': self.task[0]})
                    dbConn_img.DBConn.set_image_TimeoutStatus(self.task[0])
                    self.completed_task = (*self.task, False)
                    print(f'task({self.task[0]}) failed')
                    logging.info(f'task({self.task[0]}) failed')
                    self.work_done = True
                    return False
            except:
                pass

    def sharpen_model(self, sharpen):
        if sharpen == 1:
            sharpen_array = '0 -1 0 -1 5 -1 0 -1 0:\
                0 -1 0 -1 5 -1 0 -1 0:\
                0 -1 0 -1 5 -1 0 -1 0:\
                0 -1 0 -1 5 -1 0 -1 0'
        elif sharpen == 2:
            sharpen_array = '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 25 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1:\
                -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 25 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1:\
                -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 25 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1:\
                -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 25 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
        elif sharpen == 3:
            sharpen_array = '-1 -1 -1 -1 -1 -1 -1 -1 0 0 0 0 0 -1 -1 0 1 1 1 0 -1 -1 0 1 17 1 0 -1 -1 0 1 1 1 0 -1 -1 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1:\
                -1 -1 -1 -1 -1 -1 -1 -1 0 0 0 0 0 -1 -1 0 1 1 1 0 -1 -1 0 1 17 1 0 -1 -1 0 1 1 1 0 -1 -1 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1:\
                -1 -1 -1 -1 -1 -1 -1 -1 0 0 0 0 0 -1 -1 0 1 1 1 0 -1 -1 0 1 17 1 0 -1 -1 0 1 1 1 0 -1 -1 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1:\
                -1 -1 -1 -1 -1 -1 -1 -1 0 0 0 0 0 -1 -1 0 1 1 1 0 -1 -1 0 1 17 1 0 -1 -1 0 1 1 1 0 -1 -1 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1'
        else:
            return ''

class VidUpscaler(Worker):
    def __init__(self, task, gpu_avail):
        print('video upscaler init')
        logging.info('video upscaler init')
        super().__init__(task, gpu_avail)
        self.id = task[0]
        # vename, video_fullpath -> origin_file_path
        self.origin_file_path = task[1]
        self.aimodel_name = task[2]
        self.vename_splitext = os.path.splitext(self.origin_file_path.split('/')[-1])
        self.sr_output_file_name = self.vename_splitext[0] + self.vename_splitext[1]
        self.sr_video_fullpath = MEDIA_ROOT + '/' + self.sr_output_file_name
        self.aimodel_path = AIMODEL_PATH + self.aimodel_name +'_3c.pb' 
        

    async def do_job(self):
        self.is_working = True
        print(f'{self.idx} job start ')
        logging.info(f'{self.idx} job start ')
        self.get_file_info()
        result= asyncio.create_task(self.do_upscale())
        print('job done. work result=', result)
        logging.info('job done. work result= %s', result)
        await asyncio.sleep(1)
        # self.work_done = True

    def get_file_info(self):
        # 파일 정보가져오기
        print(f'worker {self.idx} get file_info')
        sio.emit('send_event', {"event": "video_start_video_upscaling","userId": self.task[3],'idx': self.task[0] })
        batcmd = F"""/usr/local/bin/ffprobe -v quiet -print_format json -show_format -show_streams -select_streams v:0 {self.origin_file_path}"""
        result = json.loads(subprocess.check_output(batcmd, shell=True))
        self.codec = result["streams"][0]["codec_tag_string"].lower()  
        self.video_time = result["format"]["duration"]
        self.video_duration = str(float(self.video_time)*100*1000)
        # self.cursor = dbConn_img.DBConn.getCursor() # 이건 왜?
        dbConn_video.DBConn.set_video_RunningStatus(self.id, self.sr_output_file_name, self.start_dt, self.video_duration) 
        print('codec=>',self.codec)

    async def do_upscale(self):
        print("start to upscale")
        logging.info("start to upscale")
        self.is_working = True
        cmd = F"""FFREPORT=file={SRLOG_DIR}/{self.id}_{self.sr_output_file_name}.report:level=32 {gpuscript} -progress pipe:1 -y -i {self.origin_file_path} -vf "sr=dnn_backend=tensorflow:model={self.aimodel_path}:gpu_index={self.gpu_avail}" {self.sr_video_fullpath} tile_size=400"""
        print(cmd)
        logging.info(cmd)
        self.proc = await asyncio.create_subprocess_shell(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE ,encoding='utf-8', bufsize=0,shell=True, universal_newlines=False, preexec_fn=os.setsid)
        # self.proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE ,encoding='utf-8', bufsize=0,shell=True, preexec_fn=os.setsid)
        await asyncio.sleep(5)
        try:
            print("step2 - started upscaling id=", self.task[0], f'-- [{datetime.datetime.now()}]')
            logging.info(f"step2 - started upscaling id= {self.task[0]} -- [{datetime.datetime.now()}]")
            hashed_file_name = self.origin_file_path.split('/')[-1]
            hashkey = hashed_file_name.split(".")[0]
            print('hashkey =>',hashkey)
            # r.update_progress(hashkey,10,True)
            sio.emit('send_event', {'event': 'video_progress_update','userId': self.task[3],'idx': self.task[0],'progress': 10 })
            # ret = self.proc.wait()
            ret = await self.proc.wait()
            # ret = await asyncio.wait_for(self.proc, 70.0)
        except:
            print("upscale fail")
            logging.info("upscale fail")
        finally:
            try:
                print("step3 - ended upscaling,id={0},rc={1}".format(self.task[0],self.proc.returncode))
                logging.info("step3 - ended upscaling,id={0},rc={1}".format(self.task[0],self.proc.returncode))
                if self.proc.returncode==0:
                    sio.emit('send_event', {'event': 'video_progress_update','userId': self.task[3],'idx': self.task[0],'progress': 90 })
                    complete_dt = datetime.datetime.now()
                    self.completed_task = (*self.task, complete_dt) #OK
                    print('completed_task=>', self.completed_task)
                    logging.info('completed_task=> %s', self.completed_task)
                    self.work_done = True
                    return True
                # returncode가 0이 아니면 error처리
                else:
                    print('upscale fail')
                    logging.warning('upscale fail')
                    sio.emit('send_event', {'event': 'video_progress_fail','userId': self.task[3],'idx': self.task[0]})
                    dbConn_video.DBConn.set_video_TimeoutStatus(self.task[0])
                    self.completed_task = (*self.task, False)
                    print(f'task({self.task[0]}) failed')
                    logging.info(f'task({self.task[0]}) failed')
                    self.work_done = True
                    return False
            except:
                pass


def send_mail(body, title='test', to='ssamko@gdflab.com'):
    msg = MIMEText(body)
    msg['Subject'] = title
    msg['To'] = to
    from_addr = pikavue['auth']['user']
    msg['From'] = from_addr
    smtp.sendmail(from_addr=from_addr, to_addrs=to, msg=msg.as_string())


async def main():
    director = Director(max_worker_count=2)
    lcpu = os.cpu_count()*2-1
    print('CPU=>',lcpu)
    director.pre_work()
    task1 = asyncio.create_task(director.work())
    print('task start')
    await task1
    body = 'upscaler asyncio finish'
    title = 'Upscaler stopped'
    send_mail(body=body, title=title)
    print('asyncio finish')
    logging.warning('asyncio finish')
    
try:
    asyncio.run(main())
except KeyboardInterrupt:
    body = 'stopped by keyboard interrupt'
    title = 'Upscaler stopped'
    send_mail(body=body, title=title)    
    print('finish')
    logging.warning('finish')
except Exception as e:
    body = f'stopped by {e}'
    title = 'Upscaler stopped'
    send_mail(body=body, title=title)    