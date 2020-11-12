import io
import os

from google.cloud import vision

BASE_DIR = 'private'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")

client = vision.ImageAnnotatorClient()

file_name = os.path.abspath('googleAPI_study/wakeupcat.jpg')

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)