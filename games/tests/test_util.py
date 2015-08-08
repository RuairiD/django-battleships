import unittest

from django.contrib.auth.models import User
from django.test import TestCase

from games.models import Game
from games.models import Team
from games.models import Ship
from players.models import Player
from games.util import are_ships_overlapping
from games.util import is_team_next
from games.util import is_valid_ship_position


class AreShipsOverlappingTestCase(unittest.TestCase):

    def test_overlapping_ships(self):
        ship1 = Ship(
            x=2,
            y=4,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['EAST']
        )
        ship2 = Ship(
            x=4,
            y=2,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        self.assertTrue(are_ships_overlapping(ship1, ship2))

    def test_non_overlapping_ships(self):
        ship1 = Ship(
            x=2,
            y=4,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        ship2 = Ship(
            x=4,
            y=2,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        self.assertFalse(are_ships_overlapping(ship1, ship2))


class IsTeamNextTestCase(TestCase):

    def setUp(self):
        self.game = Game()
        self.game.save()

        self.user1 = User.objects.create_user('user1', '', 'password')
        self.user2 = User.objects.create_user('user2', '', 'password')
        self.user3 = User.objects.create_user('user3', '', 'password')

        self.player1 = Player(user=self.user1)
        self.player2 = Player(user=self.user2)
        self.player3 = Player(user=self.user3)
        self.player1.save()
        self.player2.save()
        self.player3.save()

        self.team1 = Team(player=self.player1, game=self.game, last_turn=1)
        self.team2 = Team(player=self.player2, game=self.game, last_turn=2)
        self.team3 = Team(player=self.player3, game=self.game, last_turn=3)
        self.team1.save()
        self.team2.save()
        self.team3.save()

    def test_team_is_next(self):
        self.assertTrue(is_team_next(self.team1, self.game))

    def test_team_is_not_next(self):
        self.assertFalse(is_team_next(self.team2, self.game))
        self.assertFalse(is_team_next(self.team3, self.game))

    def test_non_alive_team(self):
        self.team1.alive = False
        self.team1.save()

        self.assertTrue(is_team_next(self.team2, self.game))


class MakeShipsTestCase(unittest.TestCase):

    def test_valid_position(self):
        ship = Ship(
            x=2,
            y=4,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['EAST']
        )
        self.assertTrue(is_valid_ship_position(ship))

    def test_starts_too_far_north(self):
        ship = Ship(
            x=4,
            y=-1,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_ends_too_far_north(self):
        ship = Ship(
            x=4,
            y=2,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['NORTH']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_starts_too_far_south(self):
        ship = Ship(
            x=4,
            y=10,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['NORTH']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_ends_too_far_south(self):
        ship = Ship(
            x=4,
            y=8,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_starts_too_far_west(self):
        ship = Ship(
            x=-1,
            y=5,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['EAST']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_ends_too_far_west(self):
        ship = Ship(
            x=2,
            y=5,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['WEST']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_starts_too_far_east(self):
        ship = Ship(
            x=10,
            y=5,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['WEST']
        )
        self.assertFalse(is_valid_ship_position(ship))

    def test_ends_too_far_east(self):
        ship = Ship(
            x=8,
            y=5,
            length=4,
            direction=Ship.CARDINAL_DIRECTIONS['EAST']
        )
        self.assertFalse(is_valid_ship_position(ship))
