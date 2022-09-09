import socketio
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': os.path.join(DIR_PATH, 'index.html')}
})

lobbies = {}

from battleship import routes