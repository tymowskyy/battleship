from enum import Enum

class Orientation(Enum):
    HORIZONTAL = False
    VERTICAL = True

    def translate(self, position, distance):
        if self.value:
            return (position[0], position[1] + distance - 1)
        return (position[0] + distance - 1, position[1])

class PlaceShipResponses(Enum):
    INVALID_POSITION = 1
    SHIP_USED = 2
    SUCCESS = 3
    SUCCESS_ALL_SHIPS_PLACED = 4

    def is_success(self):
        return self in [self.SUCCESS, self.SUCCESS_ALL_SHIPS_PLACED]

class FireResponses(Enum):
    INVALID_POSITION = 1
    CAN_NOT_FIRE_YET = 2
    ANOTHER_PLAYERS_ROUND = 3
    MISS = 4
    HIT = 5
    SUNK = 6
    WIN = 7

    def is_success(self):
        return self in [self.MISS, self.HIT, self.SUNK, self.WIN]

def get_tiles_between(p1, p2):
    return [(x, y) for x in range(p1[0], p2[0]+1) for y in range(p1[1], p2[1]+1)]

class Game:

    def __init__(self, board_size=10, ships=None):
        self.current_player = True
        if ships is None:
            ships = [5, 4, 3, 3, 2]
        self.ships = ships
        self.board_size = board_size
        self.ship_sizes_left = [self.ships.copy(), self.ships.copy()]
        self.player_ships = [[], []]

    def is_on_board(self, position):
        return position[0] >= 0 and position[0] < self.board_size \
            and position[1] >= 0 and position[1] < self.board_size

    def place_ship(self, player, ship_size, ship_position, ship_orientation):
        if not ship_size in self.ship_sizes_left[player]:
            return PlaceShipResponses.SHIP_USED
        if not self.is_on_board(ship_position):
            return PlaceShipResponses.INVALID_POSITION

        ship_end_position = ship_orientation.translate(ship_position, ship_size)
        if not self.is_on_board(ship_end_position):
            return PlaceShipResponses.INVALID_POSITION
        for x, y in get_tiles_between((ship_position[0] - 1, ship_position[1] - 1), (ship_end_position[0] + 1, ship_end_position[1] + 1)):
            if not self.is_on_board((x, y)):
                continue
            for ship in self.player_ships[player]:
                if ship.colide((x, y)):
                    return PlaceShipResponses.INVALID_POSITION

        self.ship_sizes_left[player].remove(ship_size)
        self.player_ships[player].append(Ship(ship_position, ship_orientation, ship_size))

        if self.ship_sizes_left[False] or self.ship_sizes_left[True]:
            return PlaceShipResponses.SUCCESS
        return PlaceShipResponses.SUCCESS_ALL_SHIPS_PLACED


    def fire(self, player, position):
        if player != self.current_player:
            return FireResponses.ANOTHER_PLAYERS_ROUND
        if not self.is_on_board(position):
            return FireResponses.INVALID_POSITION
        if self.ship_sizes_left[0] or self.ship_sizes_left[1]:
            return FireResponses.CAN_NOT_FIRE_YET

        self.current_player = not self.current_player

        for ship in self.player_ships[not player]:
            if ship.colide(position):
                sunk = ship.hit(position)
                if sunk:
                    if self.all_player_ships_sunk(not player):
                        return FireResponses.WIN
                    return FireResponses.SUNK
                return FireResponses.HIT
        return FireResponses.MISS
    
    def all_player_ships_sunk(self, player):
        return all([s.is_sunk() for s in self.player_ships[player]])


class Ship:
    def __init__(self, position, orientation, size):
        self.size = size
        end_position = orientation.translate(position, size)
        self.tiles = []
        for x, y in get_tiles_between(position, end_position):
            self.tiles.append((x, y))
        self.hitted = [False] * size
    
    def colide(self, position):
        return position in self.tiles
    
    def hit(self, position):
        index = self.tiles.index(position)
        self.hitted[index] = True
        return self.is_sunk()
    
    def is_sunk(self):
        return all(self.hitted)