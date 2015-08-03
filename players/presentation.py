from collections import namedtuple

from games.models import Team
from players.models import Player


class PlayerPresenter(namedtuple('PlayerPresenter', ['username', 'win_count', 'loss_count', 'in_progress_count'])):

    @classmethod
    def from_player(cls, player):
        winning_teams = Team.objects.filter(player=player, winner=True)
        losing_teams = Team.objects.filter(player=player, alive=False)
        in_progress_teams = Team.objects.filter(player=player, winner=False, alive=True)

        return cls(
            username=player.user.username,
            win_count=len(winning_teams),
            loss_count=len(losing_teams),
            in_progress_count=len(in_progress_teams),
        )
