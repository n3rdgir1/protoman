"node to reset the state after completed flow"

from graph.state import State
from util.extensions import chat

def complete(state: State):
    """Reset the state after the flow is completed"""
    messages = [chat("Is there anything else I can help you with?")]
    return {
        **state,
        'chat': state['chat'] + messages,
        'ask': None,
        'user_input': None,
        'plan': [],
        'scratchpad': ''
    }
