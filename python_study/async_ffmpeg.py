import asyncio


cmd = 'FFREPORT=file=/srlog/757_3Rhm3wvmkxyZwQisJkKm5D22.mp4.report:level=32 /usr/local/bin/ff_gpu0 -progress pipe:1 -y -i https://storage.googleapis.com/origin/3Rhm3wvmkxyZwQisJkKm5D22.mp4 -vf "sr=dnn_backend=tensorflow:model=/mnt/gdf/ff_server/pb/R1x2_3c.pb:gpu_index=0" /data/out/3Rhm3wvmkxyZwQisJkKm5D22.mp4 tile_size=400'


async def do_upscale(cmd):
    
    # Create the subprocess; redirect the standard output
    # into a pipe.
    # proc = await asyncio.create_subprocess_exec(program,
    #     cmd,
    #     stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    # Read one line of output.
    # data = await proc.stdout.readline()
    if stderr:
        print(stderr)
    else:
        print(stdout)
    # line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit.
    await proc.wait()
    # return line

async def main():
    task = asyncio.create_task(do_upscale(cmd))
    await task

result = asyncio.run(do_upscale(cmd))
print(f"Current: {result}")
# asyncio.run(main())