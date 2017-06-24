import websocket
import _thread as thread
import time
import json
import cozmo
import sys

# wsserver = "ws://echo.websocket.org/"
# wsserver = "ws://192.168.100.157:3000/"
wsserver = "ws://localhost:3000/"

coz = None

def cozmo_action(message):
    msg_dict = json.loads(message)
    command = msg_dict["command"]
    values = msg_dict["values"]

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


def on_message(ws, message):
    print('on_message')
    print(message)
    cozmo_action(message)

def on_error(ws, error):
    print('on_error')
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            print("cozmo client running")
            time.sleep(1)
    thread.start_new_thread(run, ())

def send(msg):
    ws.send(json.dumps(msg))

def cozmo_app(coz_conn):
    global coz
    coz = coz_conn.wait_for_robot()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        wsserver,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
    cozmo.setup_basic_logging()
    try:
        cozmo.connect(cozmo_app)
    except cozmo.ConnectionError as e:
        sys.exit('A connection error occurred: {}'.format(e))
