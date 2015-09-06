from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from pyquery import PyQuery

from games.models import Game
from games.models import Ship
from games.models import Shot
from games.models import Team
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


class CreateGameViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('user1', '', 'password')
        self.user2 = User.objects.create_user('user2', '', 'password')
        self.user3 = User.objects.create_user('user3', '', 'password')

        self.player1 = Player(user=self.user1)
        self.player2 = Player(user=self.user2)
        self.player3 = Player(user=self.user3)
        self.player1.save()
        self.player2.save()
        self.player3.save()

    def test_get(self):
        url = reverse('create_game')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        # Assert there's a field for entering a username
        self.assertEqual(len(pq('[name="opponent_username_0"]')), 1)

    def test_post_logged_out(self):
        url = reverse('create_game')
        resp = self.client.post(url, {
            'opponent_username_0': self.user2.username
        })

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))

    def test_post_logged_in_invalid_username(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        url = reverse('create_game')
        resp = self.client.post(url, {
            'opponent_username_0': 'nonexistantuser'
        })

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        # Assert error is shown
        self.assertEqual(len(pq('.alert-danger')), 1)
        self.assertIn('User does not exist', pq('.alert-danger').text())

    def test_post_logged_in_valid_username(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        url = reverse('create_game')
        resp = self.client.post(url, {
            'opponent_username_0': self.user2.username
        })

        game = Game.objects.all().order_by('-id')[0]
        teams = game.teams.all()
        team_names = [team.player.user.username for team in teams]

        self.assertRedirects(
            resp,
            reverse('game', args=[game.id])
        )
        self.assertEqual(len(teams), 2)
        self.assertIn(self.user1.username, team_names)
        self.assertIn(self.user2.username, team_names)

    def test_post_logged_in_multiple_username(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        url = reverse('create_game')
        resp = self.client.post(url, {
            'opponent_username_0': self.user2.username,
            'opponent_username_1': self.user3.username
        })

        game = Game.objects.all().order_by('-id')[0]
        teams = game.teams.all()
        team_names = [team.player.user.username for team in teams]

        self.assertRedirects(
            resp,
            reverse('game', args=[game.id])
        )
        self.assertEqual(len(teams), 3)
        self.assertIn(self.user1.username, team_names)
        self.assertIn(self.user2.username, team_names)
        self.assertIn(self.user3.username, team_names)


class AttackViewTestCase(TestCase):

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

    def test_post_logged_out(self):
        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 0,
            'target_y': 0,
            'target_team': self.team2.id,
        })

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))

    def test_post_non_existent_game(self):
        self.client.login(
            username=self.user3.username,
            password='password'
        )

        url = reverse('attack', args=[2])
        resp = self.client.post(url, {
            'target_x': 0,
            'target_y': 0,
            'target_team': self.team2.id,
        })

        self.assertEqual(resp.status_code, 404)

    def test_post_logged_in_not_playing(self):
        self.client.login(
            username=self.user3.username,
            password='password'
        )

        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 0,
            'target_y': 0,
            'target_team': self.team2.id,
        })

        self.assertEqual(resp.status_code, 404)

    def test_post_logged_in_playing_not_turn(self):
        self.client.login(
            username=self.user2.username,
            password='password'
        )

        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 0,
            'target_y': 0,
            'target_team': self.team2.id,
        }, follow=True)

        game_url = 'http://testserver{}'.format(
            reverse('game', args=[self.game.id])
        )
        self.assertIn(
            (game_url, 302),
            resp.redirect_chain
        )

        pq = PyQuery(resp.content)

        # Assert error is shown
        self.assertEqual(len(pq('.alert-danger')), 1)
        self.assertIn('It\'s not your turn', pq('.alert-danger').text())

    def test_post_logged_in_playing_miss(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 0,
            'target_y': 0,
            'target_team': self.team2.id,
        }, follow=True)

        game_url = 'http://testserver{}'.format(
            reverse('game', args=[self.game.id])
        )
        self.assertIn(
            (game_url, 302),
            resp.redirect_chain
        )

        pq = PyQuery(resp.content)

        # Assert error is shown
        self.assertEqual(len(pq('.alert-warning')), 1)
        self.assertIn('Miss', pq('.alert-warning').text())

    def test_post_logged_in_playing_duplicate(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        shot = Shot(
            game=self.game,
            attacking_team=self.team1,
            defending_team=self.team2,
            x=0,
            y=0
        )
        shot.save()

        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 0,
            'target_y': 0,
            'target_team': self.team2.id,
        }, follow=True)

        game_url = 'http://testserver{}'.format(
            reverse('game', args=[self.game.id])
        )
        self.assertIn(
            (game_url, 302),
            resp.redirect_chain
        )

        pq = PyQuery(resp.content)

        # Assert error is shown
        self.assertEqual(len(pq('.alert-danger')), 1)
        self.assertIn('You\'ve already shot there', pq('.alert-danger').text())

    def test_post_logged_in_playing_hit(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        ship = Ship(
            team=self.team2,
            x=1,
            y=1,
            length=2,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        ship.save()

        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 1,
            'target_y': 1,
            'target_team': self.team2.id,
        }, follow=True)

        game_url = 'http://testserver{}'.format(
            reverse('game', args=[self.game.id])
        )
        self.assertIn(
            (game_url, 302),
            resp.redirect_chain
        )

        pq = PyQuery(resp.content)

        # Assert error is shown
        self.assertEqual(len(pq('.alert-success')), 1)
        self.assertIn('Hit', pq('.alert-success').text())

    def test_post_logged_in_playing_defeat(self):
        self.client.login(
            username=self.user1.username,
            password='password'
        )

        ship = Ship(
            team=self.team2,
            x=1,
            y=1,
            length=1,
            direction=Ship.CARDINAL_DIRECTIONS['SOUTH']
        )
        ship.save()

        url = reverse('attack', args=[self.game.id])
        resp = self.client.post(url, {
            'target_x': 1,
            'target_y': 1,
            'target_team': self.team2.id,
        }, follow=True)

        game_url = 'http://testserver{}'.format(
            reverse('game', args=[self.game.id])
        )
        self.assertIn(
            (game_url, 302),
            resp.redirect_chain
        )

        pq = PyQuery(resp.content)

        # Assert error is shown
        self.assertEqual(len(pq('.alert-success')), 2)
        self.assertIn('Hit', pq('.alert-success').text())
        self.assertIn('You defeated user2', pq('.alert-success').text())
