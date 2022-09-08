import socketio
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': os.path.join(DIR_PATH, 'index.html')}
})

users = []

@sio.event
def connect(sid, environ):
    print(f'{sid} connected')
    for user in users:
        print('sent')
        sio.emit('user_joined', {'n_users': len(users) + 1}, to=user)
    users.append(sid)

@sio.event
def disconnect(sid):
    users.remove(sid)
    print(f'{sid} disconnect')
