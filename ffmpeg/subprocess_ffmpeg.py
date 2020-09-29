import os
import subprocess

cmd = 'FFREPORT=file=/mnt/gdf/pikavue_ff-server/srlog/757_3Rhm3wvmkxyZwQisJkKm5D22.mp4.report:level=32 /usr/local/bin/ff_gpu0 -progress pipe:1 -y -i https://storage.googleapis.com/gdf-web-storage/video/staging/origin/3Rhm3wvmkxyZwQisJkKm5D22.mp4 -vf "sr=dnn_backend=tensorflow:model=/mnt/gdf/ff_server/pb/R1x2_3c.pb:gpu_index=0" /mnt/gdf/pikavue_ff-server/data/out//3Rhm3wvmkxyZwQisJkKm5D22.mp4 tile_size=400'

result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0, shell=True, universal_newlines=False)
out, err = result.communicate()
exitcode = result.returncode
if exitcode != 0:
    print(exitcode, out.decode('utf8'), err.decode('utf8'))
else:
    print('Completed')