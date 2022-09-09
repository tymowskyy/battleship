from battleship import sio, lobbies
from battleship.lobby import Lobby

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
    if lobbies[lobby_id].is_full():
        return {'success': False, 'error': 'Lobby is full!'}

    with sio.session(sid) as session:
        if 'lobby_id' in session:
            return {'success': False, 'error': 'User is already in another lobby!'}
        session['lobby_id'] = lobby_id
    lobbies[lobby_id].join_player(sid)
    return {'success': True}


@sio.event
def create_lobby(sid, data):
    new_lobby_id = Lobby.generate_unique_lobby_id(lobbies.keys())
    with sio.session(sid) as session:
        if 'lobby_id' in session:
            return {'success': False, 'error': 'User is already in another lobby!'}
        session['lobby_id'] = new_lobby_id
    lobbies[new_lobby_id] = Lobby(sid, new_lobby_id)
    return {'success': True, 'lobby_id': new_lobby_id}