import os
from typing_extensions import final
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
#Load tools from langchain framework
from langchain_mcp_adapters.tools import load_mcp_tools
#Load Open AI models from Langchain framework
from langchain_ollama import ChatOllama
#Load LangGraph core components 
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode 
from langchain_core.messages import HumanMessage

# Load .env variables
load_dotenv()

# Initialize the Stdio server
server_params = StdioServerParameters(
    command="python",
    args=["-m", "app.mcp_server.server"] # Use -m for correct root match
)


prompt = '''
You are a Youtube Content Digestor.
Your task is to use your available tools to search videos on Youtube and then extract the transcript of them to finally give a summary of it.
Use your available tools such as:
1 - search_youtube_tool -> for searching videos
2 - transcript_youtube_tool -> after searching to extract the transcript using the URLs available

Content to extract: Search and summarize content of AI Engineering videos for me

Output guidelines:

Your output shall following the exact structure below:

1. Youtube title: 
[all the titles of the videos you found with the search tool]
2. Key takeaway point
- 10 bullets points with maximum 100 tokens for each
- Summarized from all the videos transcripts
3. Published date of the videos:
[all the published dates of the videos you found with the search tool]

'''


async def main():
    # Opens connection to the stdio client
    async with stdio_client(server_params) as (read, write):
        # Initialize the Client
        async with ClientSession(read_stream=read, write_stream=write) as session:
            # Awais the session
            await session.initialize()

            tools = await load_mcp_tools(session=session)
            
            llm = ChatOllama(
                model="ministral-3:3b"
            )
            
            
            llm_kit = llm.bind_tools(tools)
            
            # Create the Tool node for execution when necessary
            tool_node = ToolNode(tools)
            
            
            # -------------------------
            # AGENT LOGIC (GRAPH)
            # -------------------------

            def assistant(state: MessagesState):
                response = llm_kit.invoke(state["messages"])
                return {"messages": [response]}

            # Create graph instance for the entire workflow
            graph = StateGraph(MessagesState)

            graph.add_node("assistant", assistant)
            graph.add_node("tools", tool_node)

            graph.set_entry_point("assistant")

            # decide if the tool is needed -> Sequential Pipeline with conditional edge
            graph.add_conditional_edges(
                "assistant",
                lambda state: "tools" if state["messages"][-1].tool_calls else END
            )

            graph.add_edge("tools", "assistant")

            app = graph.compile()

            response = await app.ainvoke({
                "messages": [
                    HumanMessage(content=prompt)
                ]
            })
            
            final = response["messages"][-1].content
            print(final)
            
                   

# Initialize the async processes
if __name__ == "__main__":
    asyncio.run(main())