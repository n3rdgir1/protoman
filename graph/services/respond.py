import os
from uuid import uuid4
from langgraph.checkpoint.sqlite import SqliteSaver

from graph.builder import graph_builder, DATA_COLLECTION


def respond(user_message, base_dir, thread_id):
    """Generate a response to a user message"""
    builder = graph_builder()
    with SqliteSaver.from_conn_string(f"{base_dir}/.protoman/checkpointer.sqlite") as memory:
        graph_config = {"configurable": {"thread_id": thread_id}}
        graph = builder.compile(
            checkpointer=memory,
            debug=True,
            interrupt_before=[DATA_COLLECTION]
        )
        history_list = list(graph.get_state_history(graph_config))

        graph.get_graph().draw_mermaid_png(output_file_path=f"{base_dir}/.protoman/graph.png")
        sha = os.popen(f"cd {base_dir} && git rev-parse HEAD").read().strip()
        initial_state = {
            'base_dir': base_dir,
            'git_sha': sha,
            'need_input': False,
            'plan': [],
            'scratchpad': '',
        }

        # set chat in based on historical state
        history_count = len(history_list)
        if history_count == 0:
            # Set up initial state with user message
            initial_state['chat'] = [{'id': uuid4(), 'sender': 'user', 'text': user_message}]
            initial_state['ask'] = user_message
        else:
            ask = history_list[0].values.get('ask')
            graph.update_state(
                config=graph_config,
                values={
                    'chat': history_list[0].values['chat'] + [{
                        'id': uuid4(),
                        'sender': 'user',
                        'text': user_message
                    }],
                    'ask': ask or user_message,
                }
            )

        # Continue after last breakpoint if there is one
        if history_count > 0 and history_list[0].next != ():
            initial_state = None

        graph.invoke(
            initial_state,
            graph_config
        )
