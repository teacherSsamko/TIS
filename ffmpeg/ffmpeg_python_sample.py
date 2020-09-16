import os

import ffmpeg

video_dir_path = 'crawler/ssg/videos'
vod_list = [x for x in os.listdir(video_dir_path) if x.endswith('.mp4')]

audio_path = os.path.join(video_dir_path,'audio')

if not os.path.exists(audio_path):
    os.mkdir(audio_path)

# vod = vod_list[1]
# vod = os.path.join(video_dir_path, vod)
vod = 'crawler/ssg/videos/1000032803536.mp4'
print(vod)
filename = vod.split("/")[-1].split(".")[0]
filename = os.path.join(audio_path, filename)
print(filename)
# cmd = f'ffmpeg -i {vod} -c:a aac -ab 192000 -vn {filename}.m4a'
cmd = f'ffmpeg -i {vod} {filename}.wav'
# ffmpeg -i video.mp4 -f mp3 -ab 192000 -vn music.mp3
result = os.system(cmd)

cmd = f'base64 {filename}.wav > {filename}.txt'
result = os.system(cmd)
print(result)

# for vod in vod_list:
#     vod = os.path.join(video_dir_path, vod)
#     print(vod)
#     filename = vod.split("/")[-1].split(".")[0]
#     filename = os.path.join(audio_path, filename)
#     print(filename)
#     # cmd = f'ffmpeg -i {vod} -c:a aac -ab 192000 -vn {filename}.m4a'
#     cmd = f'ffmpeg -i {vod} {filename}.wav'
#     # ffmpeg -i video.mp4 -f mp3 -ab 192000 -vn music.mp3
#     result = os.system(cmd)

#     cmd = f'base64 {filename}.wav > {filename}.txt'
#     result = os.system(cmd)
#     print(result)
#     break
        

