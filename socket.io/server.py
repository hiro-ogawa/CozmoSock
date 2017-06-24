from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    # send(json, json=True)

if __name__ == '__main__':
    socketio.run(app)
