from googleapiclient.discovery import build
from datetime import timedelta
from decouple import config
import re

API_KEY = config('API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

hours = re.compile(r'(\d+)H')
mins = re.compile(r'(\d+)M')
seconds = re.compile(r'(\d+)S')

def calc(url):
    total_seconds = 0

    nextPageToken = None
    while True:
        request = youtube.playlistItems().list(
            part = 'contentDetails',
            playlistId = url,
            maxResults = 50,
            pageToken = nextPageToken
        )

        response = request.execute()

        vid_ids = []

        for item in response['items']:
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list(
            part = 'contentDetails',
            id = ','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = item['contentDetails']['duration']
            h = hours.search(duration)
            m = mins.search(duration)
            s = seconds.search(duration)

            h = int(h.group(1)) if h else 0
            m = int(m.group(1)) if m else 0
            s = int(s.group(1)) if s else 0

            vid_seconds = timedelta(
                hours = h,
                minutes = m,
                seconds = s
            ).total_seconds()

            total_seconds += vid_seconds
        
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break

    total_seconds = int(total_seconds)
    return total_seconds