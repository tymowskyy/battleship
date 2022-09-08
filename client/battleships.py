import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def user_joined(data):
    print('user joined ', data)

@sio.event
def disconnect():
    print('disconnected from server')

def main():
    sio.connect('http://localhost:5000')
    while True:
        input()

if __name__ == '__main__':
    main()