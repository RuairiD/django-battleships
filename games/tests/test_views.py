from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from pyquery import PyQuery

from games.models import Game
from games.models import Team
from games.models import Shot
from games.models import Ship
from players.models import Player


class GameViewTestCase(TestCase):

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

        self.team1 = Team(player=self.player1, game=self.game)
        self.team2 = Team(player=self.player2, game=self.game)
        self.team1.save()
        self.team2.save()

    def test_non_existant_game(self):
        url = reverse('game', args=[2])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_logged_out(self):
        url = reverse('game', args=[self.game.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_logged_in_playing_current_turn(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        url = reverse('game', args=[self.game.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        # Assert we have one board for each player
        self.assertEqual(len(pq('.board')), 2)
        self.assertIn('user1\'s board', pq('.board h3').text())
        self.assertIn('user2\'s board', pq('.board h3').text())
        # Assert the player is given an attack form
        self.assertEqual(len(pq('#attack-form')), 1)

    def test_logged_in_playing_not_current_turn(self):
        self.client.login(
            username=self.user2.username,
            password='password'
        )

        url = reverse('game', args=[self.game.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        # Assert we have one board for each player
        self.assertEqual(len(pq('.board')), 2)
        self.assertIn('user1\'s board', pq('.board h3').text())
        self.assertIn('user2\'s board', pq('.board h3').text())
        # Assert the player is not given an attack form
        self.assertEqual(len(pq('#attack-form')), 0)

    def test_logged_in_not_playing(self):
        self.client.login(
            username=self.user3.username,
            password='password'
        )

        url = reverse('game', args=[self.game.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)
