"""
1. extract audio from video using ffmpeg
2. upload to gcs
3. list of uploaded files
4. transcript
"""

import os
import datetime

import ffmpeg
from google.cloud import storage
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums


BASE_DIR = 'private'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")

mall = 'hmall'
mall_path = f'crawler/{mall}'
video_dir_path = f'{mall_path}/videos'

vod_list = [x for x in os.listdir(video_dir_path) if x.endswith('.mp4')] # {filename}.mp4

audio_path = os.path.join(video_dir_path,'audio')
today = datetime.date.today()

if not os.path.exists(audio_path):
    os.mkdir(audio_path)

audio_list = []
# extract audio from video using ffmpeg
for vod in vod_list:
    vod = os.path.join(video_dir_path, vod)
    print(vod)
    filename = vod.split("/")[-1].split(".")[0]
    filename = os.path.join(audio_path, filename)
    print(filename)
    cmd = f'ffmpeg -i {vod} -ac 1 {filename}.wav'
    result = os.system(cmd)

    audio_list.append(f'{filename}.wav') # {file_full_path}.wav
    print('audio list >>', audio_list)
    print(f'{filename}.wav >>> finished')
# audio_list = [x for x in os.listdir(f'{video_dir_path}/audio')]

# upload to gcs
def upload_to_gcs(file_path):
    client = storage.Client()
    bucket = client.get_bucket('aircode')
    filename = file_path.split('/')[-1]
    today = datetime.date.today()
    blob = bucket.blob(f'{mall}/{today}/{filename}')
    blob.upload_from_filename(file_path)
    print('file uploaded')

uploaded = []
while audio_list:
    audio = audio_list.pop()
    # audio_path = f'{video_dir_path}/audio/' + audio # temp code line
    audio_path = audio 
    upload_to_gcs(audio_path)
    uploaded.append(audio)
    print(len(audio_list),'audios left >>',audio_list)
    # print('file uploaded')


# transcript
def sample_long_running_recognize(video_dir_path,file_path):
    """
    Transcribe a long audio file using asynchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "ko-KR"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "encoding": encoding,
    }
    
    audio = {"uri": file_path}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    file_name = file_path.split("/")[-1].split(".")[0]
    script_path = f'{video_dir_path}/script/{file_name}.txt'
    print(script_path)
    with open(script_path,'w') as f:
        for result in response.results:
            # First alternative is the most probable result
            for alternative in result.alternatives:
                print(u"Transcript: {}".format(alternative.transcript))
                f.write(f'{alternative.transcript}\n')


def gcs_transcript():
    storage_client = storage.Client()

    blobs = storage_client.list_blobs(
        path_prefix, prefix='', delimiter=None
    )
    
    client = speech_v1.SpeechClient()

    language_code = "ko-KR"

    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "encoding": encoding,
    }

    for blob in blobs:
        print(blob.name)
        audio = {"uri": blob.path}

        operation = client.long_running_recognize(config, audio)

        print(u"Waiting for operation to complete...")
        response = operation.result()
        file_name = file_path.split("/")[-1].split(".")[0]
        script_path = f'{video_dir_path}/script/{file_name}.txt'
        print(script_path)
        with open(script_path,'w') as f:
            for result in response.results:
                # First alternative is the most probable result
                for alternative in result.alternatives:
                    print(u"Transcript: {}".format(alternative.transcript))
                    f.write(f'{alternative.transcript}\n')


while uploaded:
    audio = uploaded.pop()
    file_name = audio.split("/")[-1]
    file_path = f'gs://aircode/{mall}/{today}/{file_name}'
    print(file_path)
    sample_long_running_recognize(video_dir_path, file_path)
    # gcs_transcript()
    print('uploaded left >>',uploaded)