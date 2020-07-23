# download all gcs file
import os
import datetime

from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/PATH/TO/KEY.json"

if not os.path.exists('./DOWNLOAD'): 
    os.makedirs('./DOWNLOAD') 


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    file_list = []
    storage_client = storage.Client()

    blobs = storage_client.list_blobs(
        bucket_name, prefix=prefix, delimiter=delimiter
    )

    print("Blobs:")
    i = 0
    today = datetime.date.today()
    # check today's folder
    if not os.path.exists(f'./DOWNLOAD/{today}'): 
        os.makedirs(f'./DOWNLOAD/{today}')

    yesterday = datetime.date.today() - datetime.date.resolution
    list_name = f'DOWNLOAD/download_list_{today}.txt'
    
    for blob in blobs:
        update_day = blob.updated.date()
        if update_day >= yesterday and update_day < today:
            print(blob.name)
            filename = blob.name.split('/')[-1]
            updated = blob.updated.strftime("%Y-%m-%d %H:%M:%S")
            print(f'{filename} | {updated}')
            print(f'file size: {blob.size}')               
            
            # f.write(f'{i:04d} | {filename:16} | {updated}\n')
            file_list.append(f'{i:04d} | {filename:16} | {updated}\n')

            # blob download 

            destination_file_name = f'DOWNLOAD/{today}/{filename}'
            blob.download_to_filename(destination_file_name)

            print(
                "Blob [{}] downloaded to [{}]".format(
                    filename, destination_file_name
                )
            )
            i += 1

    with open(list_name, 'w') as f:
        for file_info in file_list:
            f.write(file_info)

    
                

list_blobs_with_prefix('BUCKET','PREFIX')


