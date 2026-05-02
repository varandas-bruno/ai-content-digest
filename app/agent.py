from dotenv import load_dotenv                                          # Environmental variables
# Load our MCP modules
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# Load tools from langchain framework
from langchain_mcp_adapters.tools import load_mcp_tools                 # load MCP tools from a MCP server
from langchain_core.messages import HumanMessage, SystemMessage         # prompt to be sent to the LLM 
# Load Open AI models from Langchain framework
from langchain_ollama import ChatOllama                                 # our LLM model which in this case we'll used Ollama
# Load LangGraph core components 
from langgraph.graph import StateGraph, MessagesState, START            # our imports for States, MessagesState, and START for edges
from langgraph.prebuilt import ToolNode, tools_condition                # tools_condition is a helper function to create conditions based on tool calls

import asyncio
import os
import pprint


###########################
# Configuration 
###########################

# Load .env variables
load_dotenv()

# Initialize the Stdio server
server_params = StdioServerParameters(
    command="python",
    args=["-m", "app.mcp_server.server"] # Use -m for correct root match
)

# Define the LLM model
llm = ChatOllama(
                model="qwen3-vl:4b",
                temperature=0.0
            )


# Go get our system prompt -> separation of concerns
def get_system_prompt():
    # Get the dynamic filepath of the system_prompt.d file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file_path = os.path.join(base_dir, "prompts", "system_prompt.md")
    
    with open(prompt_file_path, "r") as file:
        system_prompt = file.read()
        return system_prompt


###########################
# Graph setup 
###########################

def build_graph(llm_with_toolkit, tools):
    
    # Assistant definition which is the Central Brain Orchestrator
    def assistant(state: MessagesState):
        '''
        Central brain LLM node - will reason and decide wether to call a tool
        Invoke the LLM with the toolkit binded and receive the message from the State
        '''
        
        response = llm_with_toolkit.invoke(state["messages"])
        return {"messages": [response]}
    
    # Initialize our Graph State passing the MessagesState class argument
    graph = StateGraph(MessagesState)
    
    # Add the two nodes available -> assistant | tool 
    graph.add_node("assistant", assistant)
    graph.add_node("tools", ToolNode(tools))
    
    # Edge/Workflow setup
    graph.add_edge(START, "assistant")
    graph.add_conditional_edges("assistant", tools_condition)   # tools_condition will automatically decide which graph is next
    graph.add_edge("tools","assistant")
    
    return graph.compile()
    
    
###########################
# Main function
###########################


async def main():
    # Opens connection to the stdio client
    async with stdio_client(server_params) as (read, write):
        # Initialize the Client
        async with ClientSession(read_stream=read, write_stream=write) as session:
            # Awais the session
            await session.initialize()

            # Load our tools from the MCP server
            tools = await load_mcp_tools(session=session)

            llm_with_toolkit = llm.bind_tools(tools)                # bind_tools -> from Langchain to bind tools to a LLM
            
            # Build graph with our LLM and MCP tools loaded
            graph = build_graph(llm_with_toolkit, tools)        
            
            # Ask what the user wants to search for
            user_input = input("What content do you want to search on Youtube? I will summarize it! ")
            
            # Retrieve our system prompt
            system_prompt = get_system_prompt()
            
            # Invoke the graph and pass in the information
            result = await graph.ainvoke({
                "messages":[
                    SystemMessage(content= system_prompt),
                    HumanMessage(content = user_input)
                ]
            })
            
            pprint.pprint(result)
             

# Initialize the async processes
if __name__ == "__main__":
    asyncio.run(main())