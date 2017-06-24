#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from werkzeug.exceptions import abort
import json
import time

app = Flask(__name__)

test_msg_list = [
    {"command": "move_head", "values": [-5]},
    {"command": "move_lift", "values": [-5]},
    {"command": "drive_wheels", "values": [25, 50]},
    {"command": "move_head", "values": [5]},
    {"command": "move_lift", "values": [5]},
    {"command": "drive_wheels", "values": [-25, -50]},
    {"command": "move_head", "values": [-5]},
    {"command": "move_lift", "values": [-5]},
    {"command": "drive_wheels", "values": [25, 50]},
    {"command": "move_head", "values": [5]},
    {"command": "move_lift", "values": [5]},
    {"command": "drive_wheels", "values": [-25, -50]},
]

@app.route('/')
def echo():
    # environ['wsgi.websocket'] から WebSocket オブジェクトが得られる
    ws = request.environ['wsgi.websocket']
    if not ws:
        abort(400)

    i = 0
    n = len(test_msg_list)
    while True:
        message = json.dumps(test_msg_list[i%n])
        #
        print(message)
        # 入力をエコーバックする
        ws.send(message)

        time.sleep(1)

        i += 1
        # if i == n:
        #     break

if __name__ == '__main__':
    # WebSocketHandler が environ['wsgi.websocket'] をセットする
    http_server = WSGIServer(('', 3000), app, handler_class=WebSocketHandler)
    print("Test WebSocket Server Started")
    http_server.serve_forever()
