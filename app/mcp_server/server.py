from mcp.server.fastmcp import FastMCP
from app.core.sources.youtube import get_content_digest
from app.core.search.youtube_search import search_youtube

# Initialize FastMCP server
mcp = FastMCP("youtube_search_and_transcript")

@mcp.tool()
def search_youtube_tool(query: str, max_results: int = 10) -> list[dict]:
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
        return search_youtube(query, max_results)
    except Exception as e:
        print(f"Error in search_youtube_tool: {e}")
        return []
    
    

@mcp.tool()
def transcript_youtube_tool(url: str) -> str:
    '''
    Tool to get the content digest of a YouTube video given its URL.
    Based on the URLs provided, digest the content of the transcripts.
    
    Arguments:
    url: str - The URL of the YouTube video
    
    Returns:
    str - The content digest of the video
    '''
    
    try:
        return get_content_digest(url)
    except Exception as e:
        print(f"Error in transcript_youtube_tool: {e}")
        return "Error in getting transcript digest"




if __name__ == "__main__":
    mcp.run()