from pytube import YouTube

# pip install pytube3 (for python3)
YouTube('http://www.youtube.com/watch?v=Wm2Mv3HQMqE').streams.first().download()