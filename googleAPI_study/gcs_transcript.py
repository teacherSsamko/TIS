import os

from google.cloud import storage
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums


video_dir_path = 'crawler/ssg/videos'

def gcs_transcript(video_dir_path):
    storage_client = storage.Client()

    blobs = storage_client.list_blobs(
        'aircode', prefix='', delimiter=None
    )
    
    client = speech_v1.SpeechClient()

    language_code = "ko-KR"

    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "encoding": encoding,
    }

    skip_list = ['1000032002347.wav', '1000032803536.wav']
    error_list = []

    for blob in blobs:
        if not blob.name in skip_list:
            print(blob.name)
            audio = {"uri": "gs://aircode/"+blob.name}
            try:
                operation = client.long_running_recognize(config, audio)
            except:
                error_list.append(blob.name)
                continue

            print(u"Waiting for operation to complete...")
            response = operation.result()
            file_name = blob.name.split(".")[0]
            script_path = f'{video_dir_path}/script/{file_name}.txt'
            print(script_path)
            with open(script_path,'w') as f:
                for result in response.results:
                    # First alternative is the most probable result
                    for alternative in result.alternatives:
                        print(u"Transcript: {}".format(alternative.transcript))
                        f.write(f'{alternative.transcript}\n')

    print('Error list >>> ',error_list)

BASE_DIR = 'private'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")

gcs_transcript(video_dir_path)