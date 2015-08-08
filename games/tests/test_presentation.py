from django.contrib.auth.models import User
from django.test import TestCase

from games.models import Game
from games.models import GAME_SIZE
from games.models import Ship
from games.models import Shot
from games.models import Team
from games.presentation import GamePresenter
from games.presentation import TeamPresenter
from games.presentation import TilePresenter
from players.models import Player


class GamePresenterTestCase(TestCase):

    def setUp(self):
        self.game = Game()
        self.game.save()

        self.user1 = User.objects.create_user('user1', '', 'password')
        self.user2 = User.objects.create_user('user2', '', 'password')

        self.player1 = Player(user=self.user1)
        self.player2 = Player(user=self.user2)
        self.player1.save()
        self.player2.save()

        self.team1 = Team(player=self.player1, game=self.game)
        self.team2 = Team(player=self.player2, game=self.game)
        self.team1.save()
        self.team2.save()

    def test_from_game(self):
        presenter = GamePresenter.from_game(self.game)

        self.assertEqual(presenter.id, self.game.id)
        self.assertEqual(len(presenter.teams), 2)


class TeamPresenterTestCase(TestCase):

    def setUp(self):
        self.game = Game()
        self.game.save()

        self.user = User.objects.create_user('user', '', 'password')

        self.player = Player(user=self.user)
        self.player.save()

        self.team = Team(player=self.player, game=self.game)
        self.team.save()

    def test_from_team(self):
        presenter = TeamPresenter.from_team(team=self.team, game=self.game)

        self.assertEqual(presenter.player.username, self.user.username)
        self.assertTrue(presenter.is_next)
        self.assertEqual(presenter.winner, self.team.winner)
        self.assertEqual(presenter.alive, self.team.alive)
        self.assertEqual(len(presenter.tiles), GAME_SIZE)
        self.assertEqual(len(presenter.tiles[0]), GAME_SIZE)

    def test_make_tiles(self):
        tiles = TeamPresenter.make_tiles(team=self.team, game=self.game)

        self.assertEqual(len(tiles), GAME_SIZE)
        for i in range(0, GAME_SIZE):
            self.assertEqual(len(tiles[i]), GAME_SIZE)


class TilePresenterTestCase(TestCase):

    def setUp(self):
        self.game = Game()
        self.game.save()

        self.user1 = User.objects.create_user('user1', '', 'password')
        self.user2 = User.objects.create_user('user2', '', 'password')

        self.player1 = Player(user=self.user1)
        self.player2 = Player(user=self.user2)
        self.player1.save()
        self.player2.save()

        self.team1 = Team(player=self.player1, game=self.game)
        self.team2 = Team(player=self.player2, game=self.game)
        self.team1.save()
        self.team2.save()

        self.ship = Ship(
            team=self.team2,
            x=3,
            y=3,
            length=3,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        self.ship.save()

        self.shot_miss = Shot(
            game=self.game,
            attacking_team=self.team1,
            defending_team=self.team2,
            x=2,
            y=3
        )
        self.shot_miss.save()

        self.shot_hit = Shot(
            game=self.game,
            attacking_team=self.team1,
            defending_team=self.team2,
            x=3,
            y=5
        )
        self.shot_hit.save()

    def test_from_team(self):
        presenter = TilePresenter.from_team(
            x=0,
            y=1,
            team=self.team2,
            game=self.game
        )

        self.assertEqual(presenter.x, 0)
        self.assertEqual(presenter.y, 1)
        self.assertEqual(presenter.name, 'A1')
        self.assertTrue(presenter.is_empty)
        self.assertFalse(presenter.is_hit)

    def test_from_team_with_miss(self):
        presenter = TilePresenter.from_team(
            x=2,
            y=3,
            team=self.team2,
            game=self.game
        )

        self.assertEqual(presenter.x, 2)
        self.assertEqual(presenter.y, 3)
        self.assertEqual(presenter.name, 'C3')
        self.assertTrue(presenter.is_empty)
        self.assertTrue(presenter.is_hit)

    def test_from_team_with_ship(self):
        presenter = TilePresenter.from_team(
            x=3,
            y=4,
            team=self.team2,
            game=self.game
        )

        self.assertEqual(presenter.x, 3)
        self.assertEqual(presenter.y, 4)
        self.assertEqual(presenter.name, 'D4')
        self.assertFalse(presenter.is_empty)
        self.assertFalse(presenter.is_hit)

    def test_from_team_with_hit_ship(self):
        presenter = TilePresenter.from_team(
            x=3,
            y=5,
            team=self.team2,
            game=self.game
        )

        self.assertEqual(presenter.x, 3)
        self.assertEqual(presenter.y, 5)
        self.assertEqual(presenter.name, 'D5')
        self.assertFalse(presenter.is_empty)
        self.assertTrue(presenter.is_hit)
