import io
import os
import re

from google.cloud import vision

BASE_DIR = 'private'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")

# client = vision.ImageAnnotatorClient()

# file_name = os.path.abspath('googleAPI_study/wakeupcat.jpg')

# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()

# image = vision.Image(content=content)

# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    test_list = []

    for text in texts:
        print('\n"{}"'.format(text.description))
        test_list.append(text.description)

        # 위치 정보
        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return test_list

texts = detect_text('/Users/ssamko/Downloads/detail_img/19W_OKS_WJP4_04_03.jpg')
print(''.join(texts))
with open('test.txt','w') as f:
    text = ' '.join(texts)
    text = re.sub('\n', ' ', text)
    f.write(text)

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    text_list = []

    for text in texts:
        print('\n"{}"'.format(text.description))
        text_list.append(text.description)
        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return text_list

# texts = detect_text_uri('http://img.shoppingntmall.com/htmleditor/876/201015%20%EC%98%A4%EB%A0%90%EB%A6%AC%EC%95%88%20%ED%9E%88%ED%8A%B8%EB%AA%A8%20%EC%BB%AC%EB%A0%89%EC%85%98%2001160275000767616028137262301604300914504.jpg')
# print(''.join(texts))