from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Literal
import random
from PIL import Image
from io import BytesIO


# state defnition

class TripState(TypedDict):
    current_location: str

#node defnition

def erode(state: TripState) -> TripState:
    print("Arriving Erode...")
    return {"current_location": "Departed from erode"}

def coimbatore(state: TripState) -> TripState:
    print("Arriving Coimbatore...")
    return {"current_location": "Departed from Coimbatore"}

def gobi(state: TripState) -> TripState:
    print("Arriving Gobi...")
    return {"current_location": "Departed from Gobi"}

# decision edge
def make_decision_on_next_city(state: TripState) -> Literal["coimbatore","gobi"]:
    if(random.random() < 0.5):
        return "coimbatore"
    else:
        return "gobi"

#building

builder = StateGraph(TripState)

builder.add_node("erode", erode)
builder.add_node("gobi", gobi)
builder.add_node("coimbatore", coimbatore)

#build edges

builder.add_edge(START, "erode")
builder.add_conditional_edges("erode", make_decision_on_next_city)
builder.add_edge("gobi", END)
builder.add_edge("coimbatore", END)

#start travel

graph = builder.compile()

png_bytes = graph.get_graph().draw_mermaid_png()

img = Image.open(BytesIO(png_bytes))
img.show()

print(graph.invoke({"current_location": "Erode"}))
