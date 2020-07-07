from moviepy.editor import *

videoclip = VideoFileClip("/Users/ssamko/Downloads/_FNTQ9QM1.avi")

import cv2
import os

# cam = cv2.VideoCapture("/Users/ssamko/Downloads/_FNTQ9QM1.avi")
cam = cv2.VideoCapture("https://storage.googleapis.com/gdf-web-storage/video/develop/fTZtbpAU17.avi")

try: 
      
    # creating a folder named data 
    if not os.path.exists('data'): 
        os.makedirs('data') 
  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 

current_frame = 0

while(True):
    ret, frame = cam.read()

    if ret:
        name = './data/frame' + str(current_frame) + '.jpg'
        print('creating',ret)
        cv2.imwrite(name, frame)
        current_frame += 1
        break

    else:
        break

cam.release()
cv2.destroyAllWindows()
