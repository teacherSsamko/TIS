import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

img_test_dir = os.path.join(BASE_DIR,'')
all_imgs = []
for (root, dirs, files) in os.walk(img_test_dir):
    rootpath = os.path.join(os.path.abspath(img_test_dir), root)
    if len(files) > 0:
        for file_name in files:
            if '.csv' in file_name:
                filepath = os.path.join(rootpath, file_name)
                all_imgs.append(filepath)

print(all_imgs)