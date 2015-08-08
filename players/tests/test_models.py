from django.contrib.auth.models import User
from django.test import TestCase

from players.models import Player


class PlayersModelsTestCase(TestCase):

    def setUp(self):
        pass

    def test_player_creation(self):
        """Test that Game instances are created correctly."""
        user = User(username='user', password='password')
        user.save()

        player = Player(user=user)

        self.assertTrue(isinstance(player, Player))
        self.assertEqual(str(player), 'user')
