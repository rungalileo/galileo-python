# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "galileo",
#     "langgraph",
#     "langsmith",
#     "langchain",
#     "grandalf", # for printing graph in ascii
# ]
# ///
# from dotenv import load_dotenv; load_dotenv()

from typing import Annotated

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from galileo.handlers.langchain import GalileoCallback


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def node(state: State) -> dict:
    messages = state["messages"]
    new_message = AIMessage("Hello!")

    return {"messages": [*messages, new_message], "extra_field": 10}


def node2(state: State) -> dict:
    return {"messages": state["messages"]}


graph_builder = StateGraph(State)
graph_builder.add_node("node_name", node)
graph_builder.add_edge(START, "node_name")
graph_builder.add_edge("node_name", END)
graph = graph_builder.compile()

graph.get_graph().print_ascii()
graph.invoke({"messages": [{"role": "user", "content": "hi!"}]}, config={"callbacks": [GalileoCallback()]})
