"""Decline to answer."""
from graph.state import State
from util.extensions import chat

def decline(state: State):
    """Decline to answer."""
    messages = [chat("I don't know how to help you with that.")]
    return {
        **state,
        'chat': state['chat'] + messages,
    }
