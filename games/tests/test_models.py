from django.contrib.auth.models import User
from django.test import TestCase

from games.models import Game
from games.models import Team
from games.models import Shot
from games.models import Ship
from players.models import Player


class GamesModelsTestCase(TestCase):

    def setUp(self):
        pass

    def test_game_creation(self):
        """Test that Game instances are created correctly."""
        game = Game()
        game.save()

        user1 = User.objects.create_user('user1', '', 'password')
        user2 = User.objects.create_user('user2', '', 'password')

        player1 = Player(user=user1)
        player2 = Player(user=user2)
        player1.save()
        player2.save()

        team1 = Team(player=player1, game=game)
        team2 = Team(player=player2, game=game)
        team1.save()
        team2.save()

        self.assertTrue(isinstance(game, Game))
        self.assertEqual(str(game), '1 - user1 user2')

    def test_team_creation(self):
        """Test that Team instances are created correctly."""
        game = Game()
        game.save()

        user = User.objects.create_user('user', '', 'password')

        player = Player(user=user)
        player.save()

        team = Team(player=player, game=game)

        self.assertTrue(isinstance(team, Team))
        self.assertEqual(str(team), 'Game 1 - user (last_turn=0)')

    def test_shot_creation(self):
        """Test that Shot instances are created correctly."""
        game = Game()
        game.save()

        attacking_user = User.objects.create_user(
            'attacking_user',
            '',
            'password'
        )
        defending_user = User.objects.create_user(
            'defending_user',
            '',
            'password'
        )
        attacking_user.save()
        defending_user.save()

        attacking_player = Player(user=attacking_user)
        defending_player = Player(user=defending_user)
        attacking_player.save()
        defending_player.save()

        attacking_team = Team(player=attacking_player, game=game)
        defending_team = Team(player=defending_player, game=game)
        attacking_team.save()
        defending_team.save()

        shot = Shot(
            game=game,
            attacking_team=attacking_team,
            defending_team=defending_team,
            x=0,
            y=0
        )

        self.assertTrue(isinstance(shot, Shot))
        self.assertEqual(
            str(shot),
            'Game 1 - attacking_user attacked defending_user (0, 0)'
        )

    def test_ship_creation(self):
        """Test that Ship instances are created correctly."""
        game = Game()
        game.save()

        user = User(username='user', password='password')
        user.save()

        player = Player(user=user)
        player.save()

        team = Team(player=player, game=game)
        team.save()

        ship = Ship(
            team=team,
            x=0,
            y=0,
            length=3,
            direction=Ship.CARDINAL_DIRECTIONS['WEST']
        )

        self.assertTrue(isinstance(ship, Ship))
        self.assertEqual(
            str(ship),
            'Game 1 - user\'s 3L at (0, 0) facing West'
        )
