from langchain_google_genai import ChatGoogleGenerativeAI
import os
from env_helper import load_env_vars
from langgraph.graph import MessagesState, StateGraph, START
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import tools_condition, tool_node



load_env_vars()
api_key = os.getenv("GEMINI_API_KEY")

#LLM defnition
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = api_key
)


#tools defnition

def get_weather(city: str) -> str:
    """
    Retrieve the current weather information for a specified city.
    
    This function returns a description of the current weather conditions
    including temperature characteristics and climate for the given city.
    
    Args:
        city (str): The name of the city to get weather information for
    
    Returns:
        str: A descriptive string containing the weather information
    """
    return f"The {city} has chill climate today"

def get_location() -> str:
    """
    Retrieve the current location of the user.
    
    This function determines and returns the city name where the user
    is currently located. Use this when you need to know the user's
    current geographical position.
    
    Returns:
        str: The name of the city where the user is currently located
    """
    return "Bhavani"

def get_altitude(city: str) -> str:
    """
    Get the elevation/altitude information for a specified city.
    
    This function returns the height above sea level for the given city,
    providing geographical elevation data in meters.
    
    Args:
        city (str): The name of the city to get altitude information for
    
    Returns:
        str: A string describing the altitude/elevation above sea level
    """
    return "1210 Meters above from the sea level"

tools = [get_weather, get_altitude, get_location]

agent = llm.bind_tools(tools = tools)

system_message = SystemMessage(content = """You are a helpful assistant with access to specialized tools for location and weather information.

- get_location(): Gets the user's current city
- get_weather(city): Gets weather for a specific city
- get_altitude(city): Gets elevation for a specific city""")


#node defnition

def assistent(state: MessagesState):
    return {"messages": [agent.invoke([system_message] + state["messages"])]}

#build graph
builder = StateGraph(MessagesState)

builder.add_node("assistent", assistent)
builder.add_node("tools", tool_node.ToolNode(tools))
builder.add_edge(START, "assistent")
builder.add_conditional_edges("assistent", tools_condition)
builder.add_edge("tools", "assistent")

graph = builder.compile()

# png_bytes = graph.get_graph().draw_mermaid_png()

# img = Image.open(BytesIO(png_bytes))
# img.show()

#run graph
messages = [HumanMessage(content = "What is the weather today")]
messages = graph.invoke({"messages": messages})

for message in messages['messages']:
    message.pretty_print()

