import sys
import os

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from python_study.config.config import Config

"""
pip install google-api-python-client
pip install google-auth
"""


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
conf = Config()
DEVELOPER_KEY = conf.YOUTUBE_DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def next_page_search(youtube, pageToken, v_ids):
    search_response = youtube.search().list(
            pageToken=pageToken,
            part="id,snippet",
            maxResults=50,
        ).execute()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
        #   videos.append("%s (%s)" % (search_result["snippet"]["title"],
        #                              search_result["id"]["videoId"]))
            vod_name = search_result["snippet"]["title"]
            print(vod_name)
            if 'K-Choreo 8K' not in vod_name:
                print(search_result["snippet"]["title"])
                return v_ids 
            v_ids.append(search_result["id"]["videoId"])
    
    print(v_ids)
    next_page = search_response.get("nextPageToken")
    print(next_page)
    if next_page:
        v_ids.extend(next_page_search(youtube, next_page, v_ids))

    return v_ids


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    v_ids = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
        #   videos.append("%s (%s)" % (search_result["snippet"]["title"],
        #                              search_result["id"]["videoId"]))
            v_ids.append(search_result["id"]["videoId"])
        # elif search_result["id"]["kind"] == "youtube#channel":
        #   channels.append("%s (%s)" % (search_result["snippet"]["title"],
        #                                search_result["id"]["channelId"]))
        # elif search_result["id"]["kind"] == "youtube#playlist":
        #   playlists.append("%s (%s)" % (search_result["snippet"]["title"],
        #                                 search_result["id"]["playlistId"]))

    #   print("Videos:\n", "\n".join(videos), "\n")
    #   print("Channels:\n", "\n".join(channels), "\n")
    #   print("Playlists:\n", "\n".join(playlists), "\n")
    next_page = search_response.get("nextPageToken")
    if next_page:
        v_ids.extend(next_page_search(youtube, next_page, v_ids))

    print("\nfinal\n")
    # print(v_ids)
    print("V ids:\n", "\n".join(v_ids), "\n")
    print(f"V Count: {len(v_ids)}")
    url_prefix = 'https://www.youtube.com/watch?v='
    with open('googleAPI_study/data/video_list.txt', 'w') as f:
        for id in v_ids:
            f.write(f'{url_prefix}{id}\n')


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="+[K-Choreo 8K]")
    argparser.add_argument("--max-results", help="Max results", default=50)
    #   argparser.add_argument("--pageToken", help="Page Token", default="")
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))