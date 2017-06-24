#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from werkzeug.exceptions import abort
import cozmo
import json

app = Flask(__name__)


def cozmo_action(message):
    msg_dict = json.loads(message)
    command = msg_dict.get("command", "")
    values = msg_dict.get("values", [])

    if command == "drive_wheels":
        coz.drive_wheels(values[0], values[1])
    elif command == "move_head":
        coz.move_head(values[0])
    elif command == "move_lift":
        coz.move_lift(values[0])
    elif command == "roll":
        # キューブを探す
        # キューブを反転
        pass
    elif command == "stop_all_motors":
        coz.stop_all_motors()


@app.route('/')
def echo():
    # environ['wsgi.websocket'] から WebSocket オブジェクトが得られる
    ws = request.environ['wsgi.websocket']
    if not ws:
        abort(400)
    while True:
        message = ws.receive()
        print(message)
        cozmo_action(message)

def cozmo_app(coz_conn):
    global coz
    coz = coz_conn.wait_for_robot()

    # WebSocketHandler が environ['wsgi.websocket'] をセットする
    http_server = WSGIServer(('', 3000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    cozmo.setup_basic_logging()
    try:
        cozmo.connect(cozmo_app)
    except cozmo.ConnectionError as e:
        sys.exit('A connection error occurred: {}'.format(e))
