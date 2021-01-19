import os
import sys
import datetime
import re


text_dir = 'texts'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
today = datetime.date.today()
start_t = datetime.datetime.now()

if not os.path.exists(os.path.join(BASE_DIR, text_dir)):
    os.mkdir(os.path.join(BASE_DIR, text_dir))


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    BASE_DIR = 'private'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')
    text_list = list(map(lambda x: x.description, texts))

    # for text in texts:
        # print('\n"{}"'.format(text.description))
        # test_list.append(text.description)

        # 위치 정보
        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return text_list

def local_deal():
    # shopnt 를 제외한 detail_imges walk
    img_dirs = []
    for (root, dirs, files) in os.walk(os.path.join(BASE_DIR,'crawler')):
        # if dirs:
        #     for dir_name in dirs:
        #         if dir_name in ['detail', 'detail_imgs'] :
        #             print("dir: " + root + '/' + dir_name)
        if ('detail' or 'detail_imgs') in root:
            if dirs:
                for dir_name in dirs:
                    dir_path = root + '/' + dir_name
                    print("dir: " + root + '/' + dir_name)
                    img_dirs.append(dir_path)
        # if files:
        #     for file_name in files:
        #         print("file:", file_name)
    print(img_dirs)
    # img_dir = os.path.join(BASE_DIR, f'detail_images/{today}')
    for img_dir in img_dirs:
        shop_name = img_dir.split("/")[-3]
        print(shop_name)
        imgs = os.listdir(img_dir)

        # total = len(imgs)
        # for img in imgs:
        #     i = imgs.index(img)
        #     print(f'{i}/{total}')
        #     img_abs_path = os.path.join(img_dir, img)
        #     try:
        #         texts = detect_text(img_abs_path)
        #     except Exception as err:
        #         print(f"{err}\nskip this image")
            # file_name = img.split('_')[0] + f'_{shop_name}'
            # file_path = os.path.join(os.path.dirname(__file__), f'{file_name}.txt')
        #     with open(file_path, 'a') as txtfile:
        #         text = ' '.join(texts)
        #         text = re.sub('\n', ' ', text)
        #         txtfile.write(text)
        #     finish_t = datetime.datetime.now()
        #     runtime = finish_t - start_t
        #     print(runtime)

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    BASE_DIR = 'private'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')
    text_list = list(map(lambda x: x.description, texts))

    # for text in texts:
        # print('\n"{}"'.format(text.description))

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return text_list

def remote_deal_single(uri):
    texts = detect_text_uri(uri)
    with open(os.path.join(BASE_DIR, 'texts/test_uri.txt'), 'w') as f:
        f.write(''.join(texts))
    print('finished')

def remote_mongo():
    from pymongo import MongoClient

    mongo = MongoClient("mongodb://localhost:27017")
    db = mongo['aircode']
    col = db['shopnt_prod']

    with open(os.path.join(BASE_DIR, 'errors.txt'), 'r') as f:
        err = f.readlines()
    
    err_dic = {pid.strip():1 for pid in err}
    # details = list(col.find({"detail_imgs_url":{'$exists':True}, "desc":{'$exists':False}, "prod_name":{"$not":re.compile("페이지 없음")}}))
    details = list(col.find({"detail_img_url":{'$exists':True}, "desc":{'$exists':False}, "prod_name":{"$not":re.compile("페이지 없음")}}))
    total = len(details) - len(err)
    i = 1
    print(total)
    errors = ''
    with open(os.path.join(BASE_DIR, 'errors.txt'), 'a') as f:
        for d in details:
            pid = d['prod_id']
            if err_dic.get(pid.strip()):
                continue
            # urls = d['detail_imgs_url']
            urls = d['detail_img_url']
            text = ''
            for url in urls:
                try:
                    texts = detect_text_uri(url)
                except:
                    # errors += f'{pid}\n'
                    errors = f'{pid}\n'
                    f.write(errors)
                    col.find_one_and_update({'prod_id':pid}, {'$set':{"desc":'error'}})
                    break
                text += ''.join(texts)
            if text != '':
                col.find_one_and_update({'prod_id':pid}, {'$set':{"desc":text}})
            print(f'\r{i}/{total}', end='')
            i += 1
    
        


if __name__=='__main__':
    # url = 'https://img.shoppingntmall.com/m2/10277710/images/crop/0x800+0+1600/?sref=https://thefwa.speedgabia.com/shose/2018/AP_W21.jpg'
    # remote_deal_single(url)
    remote_mongo()