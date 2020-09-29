import os
import asyncio
import subprocess

cmd = 'FFREPORT=file=/mnt/gdf/pikavue_ff-server/srlog/757_3Rhm3wvmkxyZwQisJkKm5D22.mp4.report:level=32 /usr/local/bin/ff_gpu0 -progress pipe:1 -y -i https://storage.googleapis.com/gdf-web-storage/video/staging/origin/3Rhm3wvmkxyZwQisJkKm5D22.mp4 -vf "sr=dnn_backend=tensorflow:model=/mnt/gdf/ff_server/pb/R1x2_3c.pb:gpu_index=0" /mnt/gdf/pikavue_ff-server/data/out//3Rhm3wvmkxyZwQisJkKm5D22.mp4 tile_size=400'
# os.system(cmd)
async def do_upsacle(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', bufsize=0, shell=True, universal_newlines=False)
    print('proc set')
    ret = await proc.wait()
    print('end proc')


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(do_upsacle(cmd))

