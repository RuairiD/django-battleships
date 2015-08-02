from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from games.models import Game
from games.models import Team
from players.models import Player

class PlayerProfileView(View):

    template_name = 'players/player_profile.html'

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("Member does not exist")

        player = Player.objects.get(user=user)
        winning_teams = Team.objects.filter(player=player, winner=True)
        losing_teams = Team.objects.filter(player=player, alive=False)
        in_progress_teams = Team.objects.filter(player=player, winner=False, alive=True)

        context = {
            'player': player,
            'win_count': len(winning_teams),
            'loss_count': len(losing_teams),
            'in_progress_count': len(in_progress_teams)
        }
        return render(request, self.template_name, context)
