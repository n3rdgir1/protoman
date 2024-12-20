"main application"

import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from util.extensions import socketio, chat, debug
from util.init import init, should_init
from graph.services import respond, history_tree, rewind

app = Flask(__name__)

# Enable CORS and initialize SocketIO
CORS(app, resources={r"/*": {"origins": "*"}})

socketio.init_app(app, cors_allowed_origins="*")
ROOT_PATH = ""

@app.route('/chat', methods=['POST'])
def chat_with_agent():
    """ Respond to a chat message """
    print("chat endpoint")
    user_message = request.json.get('message')
    thread_id = request.json.get('thread_id')
    if not user_message:
        chat("No message provided")
        return '', 200
    try:
        debug(f"Received user message: {user_message}")
        debug(f"Thread ID: {thread_id}")
        respond(user_message, ROOT_PATH, thread_id)
        return '', 200
    except Exception as e:
        chat(str(e))
        print(e)
        traceback.print_exc()
        return '', 200

@app.route('/history/<thread_id>', methods=['GET'])
def get_history(thread_id):
    """ Get the chat history for a given thread """
    history_data = history_tree(thread_id, ROOT_PATH)
    return jsonify(history_data)

@app.route('/history/chat', methods=['POST'])
def rewind_history():
    """ Respond to a chat message """
    thread_id = request.json.get('threadId')
    checkpoint_id = request.json.get('checkpointId')
    try:
        debug(f"Thread ID: {thread_id}")
        debug(f"Checkpoint ID: {checkpoint_id}")
        rewind(ROOT_PATH, thread_id, checkpoint_id)
        return '', 200
    except Exception as e:
        chat(str(e))
        print(e)
        traceback.print_exc()
        return '', 200

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ROOT_PATH = sys.argv[1]
        if should_init(ROOT_PATH):
            init(ROOT_PATH)
    else:
        print("Please specify a workspace directory path")
        socketio.stop()
        exit(1)
    socketio.run(app, debug=True)
