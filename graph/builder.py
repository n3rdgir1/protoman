"""This module contains the graph for the chatbot."""
from langgraph.graph import StateGraph, END

from graph.state import State
from graph.nodes import *
from graph.routers import is_coding, RouteQuery


CONTINUE="continue"
GREET="greet"
DECLINE="decline"
DATA_GATHERING="data_gathering"
DATA_COLLECTION="data_collection"
COMPLETE="complete"


def route_start(state):
    """Route the user question to the appropriate node."""
    print('evaluating start')
    source: RouteQuery = is_coding(state)
    if source.datasource in [CONTINUE, GREET]:
        return source.datasource
    else:
        return DECLINE

def route_data_gathering(state):
    "Ask the user for input only if needed"
    if state['need_input']:
        return DATA_COLLECTION
    else:
        return COMPLETE

def data_collection_node(state):
    "Placeholder node for user input"
    return state

def graph_builder():
    """Build the graph for the chatbot"""
    builder = StateGraph(State)

    builder.set_conditional_entry_point(route_start,
        {GREET: GREET, DECLINE: DECLINE, CONTINUE: DATA_GATHERING,})

    builder.add_node(GREET, greet)
    builder.add_node(DECLINE, decline)
    builder.add_node(COMPLETE, complete)

    builder.add_node(DATA_GATHERING, data_gathering)
    builder.add_node(DATA_COLLECTION, data_collection_node)
    builder.add_conditional_edges(DATA_GATHERING, route_data_gathering,
        {DATA_COLLECTION: DATA_COLLECTION, COMPLETE: COMPLETE})
    builder.add_edge(DATA_COLLECTION, DATA_GATHERING)

    builder.add_edge(DECLINE, COMPLETE)
    builder.add_edge(GREET, COMPLETE)
    builder.add_edge(COMPLETE, END)

    return builder
