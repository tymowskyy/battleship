from random import randint
from battleship import sio

class Lobby:
    def __init__(self, player, id):
        self.game = None
        self.p1 = player
        self.p2 = None
        self.id = id

    def is_full(self):
        return not self.p2 is None
    
    def join_player(self, player):
        self.p2 = player
        sio.emit('oponent_joined', {}, to=self.p1)
    
    def leave_player(self, player):
        if player == self.p1:
            if self.p2 is None:
                return True
            self.p1 = self.p2
        self.p2 = None
        sio.emit('end_game', {}, to=self.p1)
        return False
            
    @staticmethod
    def generate_unique_lobby_id(used_ids, lenght = 6):
        generate_lobby_id = lambda : ''.join([str(randint(0, 9)) for _ in range(lenght)])
        lobby_id = generate_lobby_id()
        while lobby_id in used_ids:
            lobby_id = generate_lobby_id()
        return lobby_id