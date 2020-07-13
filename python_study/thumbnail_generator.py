import cv2
import os

def thumbnail_generator(video_path, filename):

    cam = cv2.VideoCapture(video_path)

    try:       
        # creating a folder named data 
        if not os.path.exists('/tmp/thumbnail'): 
            os.makedirs('/tmp/thumbnail') 
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 

    current_frame = 0

    while(True):
        ret, frame = cam.read()

        if ret:
            name = '/tmp/thumbnail/'+filename+'.jpg'
            print('creating')
            cv2.imwrite(name, frame)
            # current_frame += 1
            break
        else:
            break
    print('thumbnail finish')
    cam.release()
    cv2.destroyAllWindows()
