import unittest
from battleship.game import Game, Orientation, PlaceShipResponses, FireResponses

class TestGame(unittest.TestCase):
    def test_place_ship_responses(self):
        g = Game(ships=[2, 3])
        self.assertEqual(g.place_ship(False, 2, (3, 3), Orientation.VERTICAL), PlaceShipResponses.SUCCESS)
        self.assertEqual(g.place_ship(False, 2, (3, 3), Orientation.VERTICAL), PlaceShipResponses.SHIP_USED)
        self.assertEqual(g.place_ship(False, 3, (0, 3), Orientation.HORIZONTAL), PlaceShipResponses.INVALID_POSITION)
        self.assertEqual(g.place_ship(True, 2, (9, 9), Orientation.VERTICAL), PlaceShipResponses.INVALID_POSITION)
        g.place_ship(True, 2, (0, 0), Orientation.VERTICAL)
        g.place_ship(True, 3, (2, 0), Orientation.VERTICAL)
        self.assertEqual(g.place_ship(False, 3, (5, 5), Orientation.HORIZONTAL), PlaceShipResponses.SUCCESS_ALL_SHIPS_PLACED)

    def test_fire_responses(self):
        g = Game(ships=[2, 1])
        self.assertEqual(g.fire(True, (0, 0)), FireResponses.CAN_NOT_FIRE_YET)
        g.place_ship(True, 2, (0, 0), Orientation.HORIZONTAL)
        g.place_ship(True, 1, (0, 2), Orientation.HORIZONTAL)
        g.place_ship(False, 2, (3, 0), Orientation.HORIZONTAL)
        g.place_ship(False, 1, (3, 2), Orientation.HORIZONTAL)
        self.assertEqual(g.fire(False, (0, 0)), FireResponses.ANOTHER_PLAYERS_ROUND)
        self.assertEqual(g.fire(True, (-1, 2)), FireResponses.INVALID_POSITION)
        self.assertEqual(g.fire(True, (0, 0)), FireResponses.MISS)
        self.assertEqual(g.fire(False, (0, 0)), FireResponses.HIT)
        g.fire(True, (0, 1))
        self.assertEqual(g.fire(False, (1, 0)), FireResponses.SUNK)
        g.fire(True, (0, 2))
        self.assertEqual(g.fire(False, (0, 2)), FireResponses.WIN)

    def test_responses_success_check(self):
        self.assertTrue(FireResponses.MISS.is_success())
        self.assertFalse(PlaceShipResponses.SHIP_USED.is_success())

if __name__ == '__main__':
    unittest.main()