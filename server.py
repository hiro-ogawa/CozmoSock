#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from werkzeug.exceptions import abort
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
import json
import sys
try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

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

    elif command == "drive_straight":
        coz.drive_straight(distance_mm(values[0]), speed_mmps(values[1])).wait_for_completed()
    elif command == "turn_in_place":
        coz.turn_in_place(degrees(values[0])).wait_for_completed()
    elif command == "go_to_pose":
        coz.go_to_pose(Pose(values[0], values[1], values[2], angle_z=degrees(values[3])), relative_to_robot=True).wait_for_completed()

    elif command == "show_scul":
        pass

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
