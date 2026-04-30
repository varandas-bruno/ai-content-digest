from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from pprint import pprint
import json

# Load .env variables
load_dotenv()

# Load Youtube API Key
yt_api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=yt_api_key)


request = youtube.search().list(
    q="AI news",
    part="snippet",
    maxResults=10,
    type="video"
)

response = request.execute()

# pprint(response)

# Extract all youtube video ids
ytb_pre_url = "https://www.youtube.com/watch?v="

video_list = [
    {
    'title': item['snippet']['title'],
    'date': item['snippet']['publishedAt'],
    'channel': item['snippet']['channelTitle'],
    'videoId': item['id']['videoId'],
    'url': ytb_pre_url+item['id']['videoId']
    } 
    for item in response['items']
    ]

youtube_link = "https://www.youtube.com/watch?v=" + str(video_list[0]['videoId'])

print(video_list)