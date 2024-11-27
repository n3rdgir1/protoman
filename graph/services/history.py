from langgraph.checkpoint.sqlite import SqliteSaver

from graph.builder import graph_builder


def history(thread_id, base_dir):
    """Get the chat history for a given thread"""
    builder = graph_builder()
    config = {"configurable": {"thread_id": thread_id}}
    with SqliteSaver.from_conn_string(f"{base_dir}/.protoman/checkpointer.sqlite") as memory:
        graph = builder.compile(checkpointer=memory)
        history_list = list(graph.get_state_history(config))
        print(history_list[0])

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
            return [
                chat_item
                for chat_item in current_chat
                if chat_item['id'] not in parent_chat_ids
            ]

        return [{
            'user_input': item.values.get('user_input', ''),
            'checkpoint_id': item.config['configurable']['checkpoint_id'],
            'thread_id': thread_id,
            'created_at': item.created_at,
            'next': item.next,
            'parent_checkpoint_id': (item.parent_config or {}).get('configurable', {}).get('checkpoint_id'),
            'chat': chat_difference(
                item.values.get('chat', []),
                find_parent(item, history_list).values.get('chat', []) if find_parent(item, history_list) else []
            ),
        } for item in history_list]
