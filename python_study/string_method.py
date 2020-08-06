import os
# calculating string
# frame_rate = videodata['@r_frame_rate'].split("/")[0]

# frame_rate = '30000/1001'
# frame_rate = eval(frame_rate)
# # frame_rate = f'{frame_rate:.2f}'
# frame_rate = round(frame_rate, 2)

# print(type(frame_rate))
# print(frame_rate)
vename = 'ehlo/afewjiof.mp4'
vename_splitext = os.path.splitext(vename.split('/')[-1])
sr_output_file_name = vename_splitext[0] + vename_splitext[1]

print(sr_output_file_name)
print(vename.split("/")[-1])
print(vename_splitext[0])
print(vename_splitext[1])