from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript

url = "https://www.youtube.com/watch?v=aAItDrJ8-rE"


def detect_source(url: str) -> str:
    '''
    Detect if the source is one of the available sources:
    - Youtube
    - ArXiv
    
    Arguments:
    url: str - The URL of the content to be summarized
    
    Returns:
    str - The source of the content (e.g., "Youtube", "ArXiv")
    '''
    
    if "youtube.com" in url or "youtu.be" in url:
        return "Youtube"
    elif "arxiv.org" in url:
        return "ArXiv"
    else:
        raise ValueError(f"Unsupported source: {url}")
    

def extract_youtube_content(url: str) -> FetchedTranscript:
    '''
    Extract the transcript of a YouTube video given its URL.
    
    Arguments:
    url: str - The URL of the YouTube video
    
    Returns:
    FetchedTranscript - The transcript object fetched from YouTube
    '''
    
    # Check first if the URL is valid   
    if not url:
        raise ValueError("URL cannot be empty.")
    
    # Detect the source of the content and create Ytt API object
    source = detect_source(url)
    ytt_api = YouTubeTranscriptApi()

    # Extract the transcript based on the detected source. 
    if source == "Youtube":
        video_id = url.split(sep="v=")[-1]
        result = ytt_api.fetch(video_id)
        print(result)
        return result
    else:
        raise ValueError(f"Unsupported source: {url}")
            

def youtube_digest(ytt_object: FetchedTranscript) -> str:
    '''
    Process the transcript of a YouTube video and extract key points.
    
    Arguments:
    object: FetchedTranscript - The transcript object fetched from YouTube
    
    Returns:
    list[str] - A list of key points extracted from the transcript
    '''
    
    ytt_text = []
    for entry in ytt_object:
        text = entry.text
        ytt_text.append(text)
  
    # Create a full text string from the list 
    ytt_text_string = " ".join(ytt_text)
    
    return ytt_text_string
            

ytt_content = extract_youtube_content(url)
ytt_digest = youtube_digest(ytt_content)
print(ytt_digest)

        
    