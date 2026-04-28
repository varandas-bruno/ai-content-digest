from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from pprint import pprint
import json

# Load .env variables
load_dotenv()

# Load Youtube API Key
yt_api_key = os.getenv("YOUTUBE_API_KEY")


# Hidden function with _ 
def _youtube_search(query: str, max_results: int = 10) -> dict:
    '''
    Search for videos on Youtube based on a query and return the raw response from the API.
    
    Arguments:
    query: str - The search query to find relevant videos
    max_results: int - The maximum number of results to return (default is 10)
    
    Returns:
    dict - The raw response from the Youtube API search
    
    '''
    
    # Build our Youtube Client
    youtube = build("youtube", "v3", developerKey=yt_api_key)
    
    # Build the request for search
    try:
        request = youtube.search().list(q=query, part="snippet", maxResults=max_results, type="video")
        return request.execute()
    except Exception as e:
        raise ValueError(f"Error ocurred with url: {e}")
    
    
def _youtube_video_list(response: dict) -> list:
    '''
    Process the response from the Youtube API search and extract relevant video information.
    
    Arguments:
    response: dict - The response from the Youtube API search
    
    Returns:
    list[dict] - A list of dictionaries containing video information (title, date, channel, videoId, url)
    '''
    
    # Youtube url pre fix
    ytb_pre_url = "https://www.youtube.com/watch?v="

    # List comprehension to get a dict of all videos with metadata
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

    return video_list
    
    
def search_youtube(query: str, max_results: int = 10) -> list:
    '''
    Search for videos on Youtube based on a query and return a list of relevant videos with metadata.
    Calls the hidden functions to perform the search and process the results.
    
    Arguments:
    query: str - The search query to find relevant videos
    max_results: int - The maximum number of results to return (default is 10)
    
    Returns:
    list[dict] - A list of dictionaries containing video information (title, date, channel, videoId, url)
    '''
    
    response = _youtube_search(query, max_results)
    youtube_videos = _youtube_video_list(response)

    return youtube_videos
    
    
if __name__ == "__main__":
    search_youtube("ai videos 2026")
    
    
    
    
    
    