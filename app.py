import sys
from util.init import init, should_init
from flask import Flask
from flask_cors import CORS
from util.extensions import socketio

app = Flask(__name__)

# Enable CORS and initialize SocketIO
CORS(app, resources={r"/*": {"origins": "*"}})

socketio.init_app(app, cors_allowed_origins="*")
root_path = ""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        if should_init(root_path):
            init(root_path)
    else:
        print("Please specify a workspace directory path")
        socketio.stop()
        exit(1)
    socketio.run(app, debug=True)
