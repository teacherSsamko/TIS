import os
from datetime import datetime
 
def write_file(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)
 
def print_time():   
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "Current Time = " + current_time
    return data
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
write_file(os.path.join(BASE_DIR, 'test.txt') , print_time())