from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from games.models import Game
from games.models import Team
from players.models import Player
from players.presentation import PlayerPresenter

class PlayerProfileView(View):

    template_name = 'players/player_profile.html'

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("Member does not exist")

        player = Player.objects.get(user=user)

        context = {
            'player': PlayerPresenter.from_player(player),
        }
        return render(request, self.template_name, context)
