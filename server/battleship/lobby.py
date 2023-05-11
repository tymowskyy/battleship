from random import randint, choice
from battleship import sio
from battleship.game import FireResponses, Game, Orientation, PlaceShipResponses

class Lobby:

    get_other_player = lambda self, p: self.p1 if p == self.p2 else self.p2

    def __init__(self, player, id):
        self.game = None
        self.p1 = player
        self.p2 = None
        self.id = id
        self.starting_player = None

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
        self.game = None
        self.starting_player = None
        sio.emit('oponent_left', {}, to=self.p1)
        return False
            
    def start_game(self, who_starts):
        if who_starts == 0:
            self.starting_player = choice(self.p1, self.p2)
        elif who_starts == 1:
            self.starting_player = self.p1
        else:
            self.starting_player = self.p2

        self.game = Game()
        for player in (self.p1, self.p2):
            sio.emit('game_started', {}, to=player)

    def place_ship(self, player, pos, size, orientation):
        result = self.game.place_ship(player==self.starting_player, size, pos, orientation)
        if result == PlaceShipResponses.SUCCESS_ALL_SHIPS_PLACED:
            if player != self.starting_player:
                sio.emit('can_fire', {}, to=self.starting_player)
            else:
                return {'success': True, 'can_fire': True}
        return {'success': result.is_success()}

    def fire(self, player, pos):
        result = self.game.fire(player==self.starting_player, pos)
        win = result == FireResponses.WIN
        enemy = self.get_other_player(player)
        if result.is_success():
            if win:
                sio.emit('enemy_fired', {'winner': False, 'pos': pos, 'result': result.name}, to=enemy)
                return {'winner': True, 'result': result.name}
            sio.emit('enemy_fired', {'pos': pos, 'result': result.name}, to=enemy)
            sio.emit('can_fire', {}, to=enemy)
            return {'success': True, 'result': result.name}
        return {'success': False, 'result': result.name}


    @staticmethod
    def generate_unique_lobby_id(used_ids, lenght = 4):
        generate_lobby_id = lambda : ''.join([str(randint(0, 9)) for _ in range(lenght)])
        lobby_id = generate_lobby_id()
        while lobby_id in used_ids:
            lobby_id = generate_lobby_id()
        return lobby_id