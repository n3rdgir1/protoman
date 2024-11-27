"Socket extension and helper funcitons"

from flask_socketio import SocketIO
from uuid import uuid4

socketio = SocketIO(cors_allowed_origins="*")

CHAT = 'chat'
USER = 'user'
TERMINAL = 'terminal'
DEBUG = 'debug'

def terminal_input(command):
    "Emit the terminal input command"
    # socketio.emit(CHAT, f'Running `{command}`')
    socketio.emit(TERMINAL, f'${command}')
    print("TERMINAL", command)

def terminal_output(output):
    "Emit the terminal output"
    socketio.emit(TERMINAL, f'{output}')

def chat(message):
    "Emit the chat message"
    socketio.emit(CHAT, f'{message}')
    print("CHAT", message)
    return {'sender': 'bot', 'text': message, 'id': uuid4(),}

def debug(message):
    "Emit the debug message"
    socketio.emit(DEBUG, f'{message}')
    print("DEBUG", message)
    return {'sender': 'debug', 'text': message, 'id': uuid4(),}
