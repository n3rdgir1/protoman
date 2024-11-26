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
COMPLETE="complete"

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
    builder.add_node(COMPLETE, complete)

    builder.add_node(DATA_GATHERING, data_gathering)
    builder.add_edge(DATA_GATHERING, COMPLETE)

    builder.add_edge(DECLINE, COMPLETE)
    builder.add_edge(GREET, COMPLETE)
    builder.add_edge(COMPLETE, END)

    # if start_node:
        # builder.set_entry_point(start_node)
    return builder

def respond(user_message, base_dir, thread_id):
    """Generate a response to a user message"""
    builder = graph_builder()
    with SqliteSaver.from_conn_string(f"{base_dir}/.protoman/checkpointer.sqlite") as memory:
        history_list = history(thread_id, base_dir)

        graph = builder.compile(checkpointer=memory, debug=False, interrupt_after=[DATA_GATHERING])

        graph.get_graph().draw_mermaid_png(output_file_path=f"{base_dir}/.protoman/graph.png")
        sha = os.popen(f"cd {base_dir} && git rev-parse HEAD").read().strip()
        initial_state = {"user_input": user_message, 'base_dir': base_dir, 'git_sha': sha}

        # TODO: set chat in state based on historical state if it exists

        # Continue after last breakpoint if there is one
        if len(history_list) > 0 and history_list[0]['next'] != ():
            initial_state = None

        graph.invoke(
            initial_state,
            {"configurable": {"thread_id": thread_id}}
        )

def history(thread_id, base_dir):
    """Get the chat history for a given thread"""
    builder = graph_builder()
    config = {"configurable": {"thread_id": thread_id}}
    with SqliteSaver.from_conn_string(f"{base_dir}/.protoman/checkpointer.sqlite") as memory:
        graph = builder.compile(checkpointer=memory)
        history_list = list(graph.get_state_history(config))

        def find_parent(item, history_list):
            parent_config = item.parent_config
            if not parent_config:
                return None
            parent_id = parent_config['configurable']['checkpoint_id']
            for history_item in history_list:
                if history_item.config['configurable']['checkpoint_id'] == parent_id:
                    return history_item
            return None

        def chat_difference(current_chat, parent_chat):
            parent_chat_ids = {chat_item['id'] for chat_item in parent_chat}
            return [chat_item for chat_item in current_chat if chat_item['id'] not in parent_chat_ids]

        return [{
            'user_input': item.values.get('user_input', ''),
            'checkpoint_id': item.config['configurable']['checkpoint_id'],
            'thread_id': thread_id,
            'created_at': item.created_at,
            'next': item.next,
            'parent_checkpoint_id': (item.parent_config or {}).get('configurable', {}).get('checkpoint_id'),
            'chat': chat_difference(item.values.get('chat', []), find_parent(item, history_list).values.get('chat', []) if find_parent(item, history_list) else [])
        } for item in history_list]
