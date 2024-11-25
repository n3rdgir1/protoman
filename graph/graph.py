"""This module contains the graph for the chatbot."""
import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from graph.state import State
from graph.nodes import *
from graph.routers import is_coding, RouteQuery


CONTINUE="continue"
GREET="greet"
DECLINE="decline"
DATA_GATHERING="data_gathering"

def route_start(state):
    """Route the user question to the appropriate node."""
    print('evaluating start')
    source: RouteQuery = is_coding(state)
    if source.datasource in [CONTINUE, GREET]:
        return source.datasource
    else:
        return DECLINE

def graph_builder():
    """Build the graph for the chatbot"""
    builder = StateGraph(State)

    builder.set_conditional_entry_point(route_start,
        {GREET: GREET,
         DECLINE: DECLINE,
         CONTINUE: DATA_GATHERING,})

    builder.add_node(GREET, greet)
    builder.add_node(DECLINE, decline)
    builder.add_node(DATA_GATHERING, data_gathering)

    builder.add_edge(DECLINE, END)
    builder.add_edge(GREET, END)
    return builder

def respond(user_message, base_dir, thread_id):
    """Generate a response to a user message"""
    builder = graph_builder()
    with SqliteSaver.from_conn_string(f"{base_dir}/.protoman/checkpointer.sqlite") as memory:
        graph = builder.compile(checkpointer=memory, debug=False)

        graph.get_graph().draw_mermaid_png(output_file_path=f"{base_dir}/.protoman/graph.png")
        sha = os.popen(f"cd {base_dir} && git rev-parse HEAD").read().strip()
        graph.invoke(
            {"user_input": user_message, 'base_dir': base_dir, 'git_sha': sha},
            {"configurable": {"thread_id": thread_id}}
        )
