"Basic generation node"

from util.client import client, deployment_name
from util.extensions import chat
from graph.state import State

def greet(state: State):
    """Generate a response to a user message"""
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": state['user_input']}
        ],
    )

    messages = chat(state.get('chat', []), response.choices[0].message.content)
    return {
        **state,
        'chat': messages,
    }
