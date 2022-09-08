import socketio
import os
from random import randint

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': os.path.join(DIR_PATH, 'index.html')}
})

lobbies = {}

def generate_unique_lobby_id(lenght = 6):
    generate_lobby_id = lambda : ''.join([str(randint(0, 10)) for _ in range(lenght)])
    lobby_id = generate_lobby_id()
    while lobby_id in lobbies:
        lobby_id = generate_lobby_id()
    return lobby_id

@sio.event
def connect(sid, environ):
    print(f'{sid} connected')

@sio.event
def disconnect(sid):
    print(f'{sid} disconnect')

@sio.event
def join_lobby(sid, data):
    lobby_id = data['lobby_id']
    if not lobby_id in lobbies:
        return {'success': False, 'error': 'Lobby with this ID does not exist!'}
    if len(lobbies[lobby_id]) == 2:
        return {'success': False, 'error': 'Lobby is full!'}

    with sio.session(sid) as session:
        if 'lobby_id' in session:
            return {'success': False, 'error': 'User is already in another lobby!'}
        session['lobby_id'] = lobby_id
    lobbies[lobby_id].append(sid)
    return {'success': True}


@sio.event
def create_lobby(sid, data):
    new_lobby_id = generate_unique_lobby_id()
    with sio.session(sid) as session:
        if 'lobby_id' in session:
            return {'success': False, 'error': 'User is already in another lobby!'}
        session['lobby_id'] = new_lobby_id
    lobbies[new_lobby_id] = [sid]
    return {'success': True, 'lobby_id': new_lobby_id}