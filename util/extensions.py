"Socket extension and helper funcitons"

from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

CHAT = 'chat'
USER = 'user'
TERMINAL = 'terminal'
DEBUG = 'debug'

def terminal_input(command):
    "Emit the terminal input command"
    # socketio.emit(CHAT, f'Running `{command}`')
    socketio.emit(TERMINAL, f'${command}')

def terminal_output(output):
    "Emit the terminal output"
    socketio.emit(TERMINAL, f'{output}')

def chat(messages, message):
    "Emit the chat message"
    socketio.emit(CHAT, f'{message}')
    return messages + [{'sender': 'bot', 'text': message, 'id': len(messages),}]

def debug(messages, message):
    "Emit the debug message"
    socketio.emit(DEBUG, f'{message}')
    return messages + [{'sender': 'debug', 'text': message, 'id': len(messages),}]
