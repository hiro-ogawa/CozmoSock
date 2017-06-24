#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from werkzeug.exceptions import abort
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import json
import sys
try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

app = Flask(__name__)


image = Image.open("./scul.png")

# resize to fit on Cozmo's face screen
resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)

# convert the image to the format used by the oled screen
scul_face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)


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
        coz.display_oled_face_image(scul_face_image, values[0] * 1000.0)
        pass

    elif command == "set_lights":
        cubes = [
            coz.world.get_light_cube(LightCube1Id),  # looks like a paperclip
            coz.world.get_light_cube(LightCube2Id),  # looks like a lamp / heart
            coz.world.get_light_cube(LightCube3Id),  # looks like the letters 'ab' over 'T'
        ]

        cube = cubes[values[0]]
        color = cozmo.lights.Color(rgb = (values[1], values[2], values[3]))
        light = cozmo.lights.Light(color, color)

        if cube is not None:
            cube.set_lights(light)
        else:
            cozmo.logger.warning("Cozmo is not connected to a LightCube{}Id cube - check the battery.".format(values[0] + 1))

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
    cozmo.robot.Robot.drive_off_charger_on_connect = False
    try:
        cozmo.connect(cozmo_app)
    except cozmo.ConnectionError as e:
        sys.exit('A connection error occurred: {}'.format(e))
