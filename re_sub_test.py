# re.sub 
import re
import os

hashed_file_name = 'LC_AK2tM1'
tmp_dir = r'c:\\static\tmp'
# tmp_dir = '/static/tmp'
filePath = os.path.join(tmp_dir, hashed_file_name)
filePath = re.sub(r'\\', '/', filePath)
print(filePath)