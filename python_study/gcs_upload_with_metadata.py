import os

from google.cloud import storage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"private/gdf-service-f0c823f4a436.json")

def upload_upscaled_to_gcs(upscaled_file_path, origin_file_name):
    client = storage.Client()
    bucket = client.get_bucket('gdf-web-storage')
    filename = upscaled_file_path.split('/')[-1]
    blob = bucket.blob('image/upscaled/'+filename)
    # blob.content_disposition = 'attachment'
    blob.content_disposition = f'attachment; filename={origin_file_name}'
    blob.upload_from_filename(upscaled_file_path)
    # blob.content_encoding = 'gzip'
    # blob.patch()
    
    return f'https://storage.googleapis.com/gdf-web-storage/image/upscaled/{filename}'  

testfile_path = '/Users/ssamko/Downloads/logo_small.png'

print(upload_upscaled_to_gcs(testfile_path, 'test_2.png'))
