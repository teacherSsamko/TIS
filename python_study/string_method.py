# calculating string
# frame_rate = videodata['@r_frame_rate'].split("/")[0]

frame_rate = '30000/1001'
frame_rate = eval(frame_rate)
# frame_rate = f'{frame_rate:.2f}'
frame_rate = round(frame_rate, 2)

print(type(frame_rate))
print(frame_rate)