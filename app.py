from typing import TypedDict
from langgraph.graph import StateGraph, END

class State(TypedDict):
    message: str

def manager(state: State):
    print("🧠 Manager:", state["message"])
    return state

builder = StateGraph(State)
builder.add_node("manager", manager)
builder.set_entry_point("manager")
builder.add_edge("manager", END)

graph = builder.compile()

graph.invoke({"message": "Hello Danny AI OS!"})
