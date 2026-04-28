from mcp.server.fastmcp import FastMCP
from app.core.sources.youtube import get_content_digest

# Initialize FastMCP server
mcp = FastMCP()

@mcp.tool()
def get_content_digest_tool(url: str) -> str:
    '''
    Tool to get the content digest of a YouTube video given its URL.
    
    Arguments:
    url: str - The URL of the YouTube video
    
    Returns:
    str - The content digest of the video
    '''
    return get_content_digest(url)