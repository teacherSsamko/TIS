import os

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io

def sample_long_running_recognize(local_file_path):
    """
    Transcribe a long audio file using asynchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "ko-KR"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "encoding": encoding,
    }
    # with io.open(local_file_path, "rb") as f:
    #     content = f.read()
    # audio = {"content": content}
    audio = {"uri": local_file_path}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    with open('crawler/ssg/videos/script/test2.txt','w') as f:
        for result in response.results:
            # First alternative is the most probable result
            for alternative in result.alternatives:
                print(u"Transcript: {}".format(alternative.transcript))
                f.write(f'{alternative.transcript}\n')

def sample_recognize(local_file_path, model):
    """
    Transcribe a short audio file using a specified transcription model

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
      model The transcription model to use, e.g. video, phone_call, default
      For a list of available transcription models, see:
      https://cloud.google.com/speech-to-text/docs/transcription-model#transcription_models
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/hello.wav'
    # model = 'phone_call'

    # The language of the supplied audio
    language_code = "ko-KR"
    config = {
        "model": model, 
        "audio_channel_count": 2,
        "language_code": language_code
        }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    with open('crawler/hmall/videos/script/test.txt','w') as f:
        for result in response.results:
            # First alternative is the most probable result
            for alternative in result.alternatives:
                print(u"Transcript: {}".format(alternative.transcript))
                f.write(alternative.transcript)

BASE_DIR = 'private'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")

video_dir_path = 'crawler/ssg/videos'

# file_path = os.path.join(video_dir_path, 'audio/2107242918.txt')
# file_path = os.path.join(video_dir_path, 'audio/1000043166053.wav')
file_path = 'gs://aircode/1000032803536.wav'

sample_long_running_recognize(file_path)
# sample_recognize(file_path, 'default')