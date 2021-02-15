import unittest
import datetime

from VideoUpscaler import VideoUpscaler
from dbConn_new import DBConn_video

class TestVideoUpscaler(unittest.TestCase):
    """before test
    1. run mariaDB
    2. run eventbus
    """
    def setUp(self):
        gpu_index = 0
        self.upscaler = VideoUpscaler(gpu_index)

    def tearDown(self):
        del self.upscaler

    def setting(self):
        with DBConn_video() as db:
            sql = 'update upscale_list set file_status=6 where id=54'
            db.update_query(sql)
            sql = 'update upscale_list set file_status=3 where id=51'
            db.update_query(sql)
            get_wait = 'select id, file_status from upscale_list where file_status=6'
            waiting = db.get_query(get_wait)
            self.assertEqual(waiting[0][0], 54)
            get_run = 'select id, file_status from upscale_list where file_status=3'
            running = db.get_query(get_run)
            self.assertEqual(running[0][0], 51)

    def prework(self):
        self.setting()
        self.upscaler.prework()
        with DBConn_video() as db:
            get_wait = 'select id, file_status from upscale_list where file_status=6'
            waiting = db.get_query(get_wait)
            self.assertFalse(waiting)
            get_run = 'select id, file_status from upscale_list where file_status=3'
            running = db.get_query(get_run)
            self.assertFalse(running)
            get_failed = 'select id, file_status from upscale_list where file_status=99'
            failed = db.get_query(get_failed)
            self.assertEqual(failed[0][0], 51)
        
    def look_DB(self):
        self.upscaler.look_DB()
        with DBConn_video() as db:
            get_wait = 'select id, file_status from upscale_list where file_status=6'
            waiting = db.get_query(get_wait)
            self.assertTrue(waiting)

    def upscale(self, task):
        completed_task = self.upscaler.upscale(task, isTest=True)
        with DBConn_video() as db:
            running = 'select id, file_status from upscale_list where id=54'
            result = db.get_query(running)
            self.assertEqual(result[0][1], 3)
        return completed_task

    def after_proc(self, completed_task):
        self.upscaler.video_after_proc(completed_task, isTest=True)
        with DBConn_video() as db:
            upscaled = 'select file_status, upscaled_path from upscale_list where id=54'
            result = db.get_query(upscaled)
            self.assertEqual(result[0][0],4)
            self.assertTrue(result[0][1])

    def test_process(self):
        self.prework()
        self.look_DB()
        task = self.upscaler.tasks_to_accomplish.get()
        completed_task = self.upscale(task)
        print(completed_task)
        self.after_proc(completed_task)



if __name__ == '__main__':
    unittest.main()