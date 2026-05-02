from mcp.server.fastmcp import FastMCP
from app.core.sources.youtube import get_content_digest
from app.core.search.youtube_search import search_youtube
import logging
import asyncio

# Logger initialize
logger = logging.getLogger(__name__)


# Initialize FastMCP server
mcp = FastMCP("youtube_search_and_transcript")

@mcp.tool()
async def search_youtube_tool(query: str, max_results: int = 1) -> list[dict]:
    '''
    Use this tool to search Youtube videos when asked by the user.
    The content of the youtube videos must be the {query} variable and the maximum results shall be {max_results}
    
    Arguments:
    - query: str -> This is the query made by the user. It determines what type of Youtube video content to look for
    - max_results: int -> The max results for the search algorithm. Default is 10 videos
    
    Returns:
    - search_youtube() -> Returns a list of dict which are all the videos found with metadata included
    
    '''
    
    try:
        return await asyncio.to_thread(search_youtube, query, max_results)      # Run the blocking search_youtube function in a separate thread to avoid blocking the event loop 
    except Exception as e:
        logging.error(f"Error in search_youtube_tool: {e}")
        return []
    
    

@mcp.tool()
async def transcript_youtube_tool(url: str) -> str:
    '''
    Tool to get the content digest of a YouTube video given its URL.
    Based on the URLs provided, digest the content of the transcripts.
    
    Arguments:
    url: str - The URL of the YouTube video
    
    Returns:
    str - The content digest of the video
    '''
            
    try:
        return await asyncio.to_thread(get_content_digest, url)      # Run the blocking get_content_digest function in a separate thread to avoid blocking the event loop
    except Exception as e:
        logging.error(f"Error in transcript_youtube_tool: {e}")
        return "Error in getting transcript digest"


if __name__ == "__main__":
    mcp.run()