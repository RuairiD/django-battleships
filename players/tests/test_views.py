from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from pyquery import PyQuery

from players.models import Player


class PlayerProfileViewTestCase(TestCase):

    def test_non_existent_user(self):
        url = reverse('player_profile', args=[1])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_existent_user(self):
        user = User.objects.create_user('user1', '', 'password')
        player = Player(user=user)
        player.save()

        url = reverse('player_profile', args=[user.username])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        pq = PyQuery(resp.content)

        self.assertEqual(pq('h2').text(), user.username)
