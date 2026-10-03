from typing import TypedDict

from langgraph.graph import END, StateGraph


class State(TypedDict):
    message: str


def manager(state: State) -> State:
    print("🧠 Manager:", state["message"])
    return state


def build_graph():
    builder = StateGraph(State)
    builder.add_node("manager", manager)
    builder.set_entry_point("manager")
    builder.add_edge("manager", END)
    return builder.compile()


graph = build_graph()


def main() -> None:
    graph.invoke({"message": "Hello Danny AI OS!"})


if __name__ == "__main__":
    main()
