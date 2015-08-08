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


class SignupViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', '', 'password')

        self.player = Player(user=self.user)
        self.player.save()

    def test_get_logged_out(self):
        url = reverse('signup')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        self.assertEqual(len(pq('input#id_username')), 1)
        self.assertEqual(len(pq('input#id_password')), 1)

    def test_get_logged_in(self):
        self.client.login(
            username=self.user.username,
            password='password'
        )

        url = reverse('signup')
        resp = self.client.get(url)

        self.assertRedirects(resp, reverse('home'))

    def test_post(self):
        url = reverse('signup')
        resp = self.client.post(url, {
            'username': ['newuser'],
            'password': ['password']
        })

        player = Player.objects.all().order_by('-id')[0]

        self.assertEqual(player.user.username, 'newuser')
        self.assertTrue(player.user.check_password('password'))
        self.assertRedirects(resp, reverse('home'))
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            player.user.id
        )


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.active_user = User.objects.create_user(
            'active_user', '', 'password'
        )
        self.inactive_user = User.objects.create_user(
            'inactive_user', '', 'password'
        )

        self.inactive_user.is_active = False
        self.inactive_user.save()

        self.player1 = Player(user=self.active_user)
        self.player2 = Player(user=self.inactive_user)
        self.player1.save()
        self.player2.save()

    def test_get(self):
        url = reverse('login')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        self.assertEqual(len(pq('input#username')), 1)
        self.assertEqual(len(pq('input#password')), 1)

    def test_post(self):
        url = reverse('login')
        resp = self.client.post(url, {
            'username': 'active_user',
            'password': 'password'
        })

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            self.active_user.id
        )
        self.assertRedirects(resp, reverse('home'))

    def test_post_inactive_user(self):
        url = reverse('login')
        resp = self.client.post(url, {
            'username': 'inactive_user',
            'password': 'password'
        })

        self.assertEqual(resp.status_code, 200)

        pq = PyQuery(resp.content)
        self.assertIn(
            'Your account is disabled',
            pq('.alert-danger').text()
        )

    def test_post_bad_password(self):
        url = reverse('login')
        resp = self.client.post(url, {
            'username': 'active_user',
            'password': 'notthepassword'
        })

        self.assertEqual(resp.status_code, 200)

        pq = PyQuery(resp.content)
        self.assertIn(
            'Your username and/or password is incorrect',
            pq('.alert-danger').text()
        )


class LogoutViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', '', 'password')

        self.player = Player(user=self.user)
        self.player.save()

    def test_get(self):
        self.client.login(
            username=self.user.username,
            password='password'
        )

        url = reverse('logout')
        resp = self.client.get(url)

        self.assertRedirects(resp, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)
