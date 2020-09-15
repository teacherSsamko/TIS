from youtube_transcript_api import YouTubeTranscriptApi

video_id = 'Ch4_oKO2OWs'

# transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies='googleAPI_study/cookies.txt')
# print(transcript_list)
# transcript = transcript_list.find_transcript(['de', 'en'])
script = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'], cookies='googleAPI_study/cookies.txt')

with open('googleAPI_study/test/test_script.txt', 'w') as f:
    for subtitle in script:
        line = subtitle['text'] + '\n'
        f.write(line)
