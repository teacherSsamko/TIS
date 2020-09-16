from pytube import YouTube

# pip install pytube3 (for python3)
YouTube('https://www.youtube.com/watch?v=Yl97xekIhnw').streams.first().download()