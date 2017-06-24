from requests.exceptions import ConnectionError
from socketIO_client import SocketIO

try:
    socket = SocketIO('localhost', 5000, wait_for_connection=False)
    socket.wait()
except ConnectionError:
    print('The server is down. Try again later.')
