from django.contrib.auth.models import User
from django.test import TestCase

from games.models import Game
from games.models import Team
from players.models import Player
from players.presentation import PlayerPresenter


class PlayerPresenterTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user1', '', 'password')
        self.player = Player(user=self.user)
        self.player.save()

        self.winning_game = Game()
        self.losing_game = Game()
        self.in_progress_game = Game()
        self.winning_game.save()
        self.losing_game.save()
        self.in_progress_game.save()

        self.winning_team = Team(
            game=self.winning_game,
            player=self.player,
            alive=True,
            winner=True
        )
        self.losing_team = Team(
            game=self.losing_game,
            player=self.player,
            alive=False,
            winner=False
        )
        self.in_progress_team = Team(
            game=self.in_progress_game,
            player=self.player,
            alive=True,
            winner=False
        )
        self.winning_team.save()
        self.losing_team.save()
        self.in_progress_team.save()

    def test_from_player(self):
        presenter = PlayerPresenter.from_player(self.player)

        self.assertEqual(presenter.username, self.user.username)
        self.assertEqual(presenter.win_count, 1)
        self.assertEqual(presenter.loss_count, 1)
        self.assertEqual(presenter.in_progress_count, 1)
