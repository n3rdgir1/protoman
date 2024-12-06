"hanldes the response to the user message and picking up in the graph where left off"
import os
from uuid import uuid4
from langgraph.checkpoint.sqlite import SqliteSaver

from graph.builder import APPROVE_PLAN, graph_builder, DATA_COLLECTION


def rewind(user_message, base_dir, thread_id, checkpoint_id):
    """Generate a response to a user message"""
    builder = graph_builder()
    with SqliteSaver.from_conn_string(f"{base_dir}/.protoman/checkpointer.sqlite") as memory:
        graph_config = {"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}}
        graph = builder.compile(
            checkpointer=memory,
            debug=True,
            interrupt_before=[DATA_COLLECTION, APPROVE_PLAN],
        )
        checkpoint = list(graph.get_state_history(graph_config))[0]
        print(checkpoint.values['chat'])

        # reset git to the checkpoint sha
        sha = checkpoint.values['git_sha']
        os.system(f"cd {base_dir} && git reset --hard {sha} && git clean -fd")

        graph.update_state(
            config=checkpoint.config,
            values=checkpoint.values
        )

        graph.invoke(
            None,
            graph_config
        )
