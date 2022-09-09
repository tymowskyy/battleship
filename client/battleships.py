import socketio

sio = socketio.Client()

CREATE_OR_JOIN_LOBBY_MESSAGE = '1 - Join Lobby\n2 - Create Lobby'

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def oponent_joined(data):
    print('Oponent joined lobby!')

@sio.event
def end_game(data):
    print('Game ended')
    print(f'Lobby ID: {current_lobby}')
    

def create_or_join_lobby(user_input):
    global after_input, current_lobby

    if user_input == '1':
        lobby_id = input('Input Lobby ID: ')
        response = sio.call('join_lobby', {'lobby_id': lobby_id})
        if 'error' in response:
            print('ERROR', response['error'])
            print(CREATE_OR_JOIN_LOBBY_MESSAGE)
            return

        current_lobby = lobby_id
        print(f'Joined Lobby {current_lobby}')        
        after_input = None

    elif user_input == '2':
        response = sio.call('create_lobby', {})
        if 'error' in  response:
            print('ERROR', response['error'])
            print(CREATE_OR_JOIN_LOBBY_MESSAGE)
            return

        current_lobby = response['lobby_id']
        print(f'Your Lobby ID is {current_lobby}')
        after_input = None

    else:
        print('Invalid input!')
        print(CREATE_OR_JOIN_LOBBY_MESSAGE)

def main():
    global after_input

    sio.connect('http://localhost:5000')
    print('Input "quit" to quit the game, "leave" to leave the lobby')
    print(CREATE_OR_JOIN_LOBBY_MESSAGE)

    run = True
    while run:
        user_input = input()
        if user_input == 'exit':
            run = False
            break
        if user_input == 'leave':
            sio.emit('leave_lobby', {})
            after_input = create_or_join_lobby
            print(CREATE_OR_JOIN_LOBBY_MESSAGE)
            continue
        if not after_input is None:
            after_input(user_input)
    sio.disconnect()

after_input = create_or_join_lobby
current_lobby = None

if __name__ == '__main__':
    main()