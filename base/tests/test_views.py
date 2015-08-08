from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from pyquery import PyQuery

from games.models import Game
from games.models import Team
from players.models import Player


class HomeViewTestCase(TestCase):

    def setUp(self):
        self.game1 = Game()
        self.game2 = Game()
        self.game1.save()
        self.game2.save()

        self.user1 = User.objects.create_user('user1', '', 'password')
        self.user2 = User.objects.create_user('user2', '', 'password')

        self.player1 = Player(user=self.user1)
        self.player2 = Player(user=self.user2)
        self.player1.save()
        self.player2.save()

        self.team_game1 = Team(
            player=self.player1,
            game=self.game1
        )
        self.team_game2 = Team(
            player=self.player1,
            game=self.game2,
            alive=False
        )
        self.team_game1.save()
        self.team_game2.save()

    def test_logged_out(self):
        url = reverse('home')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        self.assertIn('You\'re not logged in', pq('h3').text())
        links = [e.attr('href') for e in pq('.container a').items()]
        self.assertIn(reverse('login'), links)
        self.assertIn(reverse('signup'), links)

    def test_logged_in_with_matches(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        url = reverse('home')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        # Assert links to 'Create New Game' plus ongoing games are shown
        self.assertIn('Your Active Games', pq('h3').text())
        links = [e.attr('href') for e in pq('.container a').items()]
        self.assertIn(reverse('game', args=[self.game1.id]), links)
        self.assertNotIn(reverse('game', args=[self.game2.id]), links)
        self.assertIn(reverse('create_game'), links)

    def test_logged_in_without_matches(self):
        self.client.login(
            username=self.user2.username,
            password='password'
        )

        url = reverse('home')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        # Assert only link to 'Create New Game' is shown
        self.assertEqual(len(pq('.container a')), 1)
        links = [e.attr('href') for e in pq('.container a').items()]
        self.assertIn(reverse('create_game'), links)
