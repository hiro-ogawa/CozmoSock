import websocket
import _thread as thread
import time
import json

# wsserver = "ws://echo.websocket.org/"
# wsserver = "ws://192.168.100.157:3000/"
wsserver = "ws://localhost:3000/"

test_msg_list = [
    # {"command": "move_head", "values": [-3]},
    # {"command": "move_lift", "values": [-3]},
    # {"command": "drive_wheels", "values": [25, 50]},
    # {"command": "move_head", "values": [3]},
    # {"command": "move_lift", "values": [3]},
    # {"command": "stop_all_motors", "values": []},
    # {"command": "move_head", "values": [3]},
    # {"command": "move_lift", "values": [3]},
    # {"command": "drive_wheels", "values": [-25, -50]},
    # {"command": "move_head", "values": [3]},
    # {"command": "move_lift", "values": [3]},
    # {"command": "stop_all_motors", "values": []},
    # {"command": "drive_straight", "values": [100, 50]},
    # {"command": "turn_in_place", "values": [90]},
    # {"command": "go_to_pose", "values": [100,100,0, 180]},
    # {"command": "set_lights", "values": [0, 255, 0, 0]},
    # {"command": "set_lights", "values": [1, 0, 255, 0]},
    # {"command": "set_lights", "values": [2, 0, 0, 255]},
    # {"command": "set_lights", "values": [0, 0, 0, 0]},
    # {"command": "set_lights", "values": [1, 0, 0, 0]},
    # {"command": "set_lights", "values": [2, 0, 0, 0]},
    {"command": "show_scul", "values": [5]},
    {"command": "none", "values": [5]},
    {"command": "none", "values": [5]},
    {"command": "none", "values": [5]},
    {"command": "none", "values": [5]},
    {"command": "none", "values": [5]},
]


def on_message(ws, message):
    print('on_message')
    print(message)

def on_error(ws, error):
    print('on_error')
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
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

        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        wsserver,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )
    ws.on_open = on_open
    ws.run_forever()
