import os

from google.cloud import storage


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/PATH/TO/KEY.json"

client = storage.Client()

bucket = client.get_bucket("gdf-web-storage")
blob = bucket.get_blob("video/")


bucket.rename_blob(blob, "video/failed/mp4")

def gcs_file_move(current_path, target_path):
    bucket = client.bucket("gdf-web-storage")
    blob = bucket.get_blob(current_path)

    bucket.rename_blob(blob, target_path)

def failed_file_move(current_path):
    bucket = client.bucket("gdf-web-storage")
    blob = bucket.get_blob(current_path)
    filename = current_path.split("/")[-1]
    target_path = f"video/failed/{filename}"

    bucket.rename_blob(blob, target_path)


    