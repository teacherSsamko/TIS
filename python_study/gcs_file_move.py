import os

from google.cloud import storage


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/PATH/TO/KEY.json"

client = storage.Client()

bucket = client.bucket("gdf-web-storage")
blob = bucket.get_blob("video/develop/3LonEKEYUvphG3fie92pKo5969.mp4")

bucket.rename_blob(blob, "video/failed/3LonEKEYUvphG3fie92pKo5969.mp4")
