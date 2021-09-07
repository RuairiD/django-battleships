from collections import namedtuple

from games.models import GAME_SIZE
from games.models import Shot
from games.util import is_team_next
from players.presentation import PlayerPresenter


class GamePresenter(namedtuple(
    'GamePresenter',
    ['id', 'teams']
)):

    @classmethod
    def from_game(cls, game):
        return cls(
            id=game.id,
            teams=[
                TeamPresenter.from_team(team, game)
                for team in game.teams.all()
            ]
        )


class TeamPresenter(namedtuple(
    'TeamPresenter',
    ['id', 'player', 'is_next', 'winner', 'alive', 'tiles']
)):

    @staticmethod
    def make_tiles(team, game):
        tiles = []
        for y in range(0, GAME_SIZE):
            row = []
            for x in range(0, GAME_SIZE):
                row.append(
                    TilePresenter.from_team(
                        x=x,
                        y=y,
                        team=team,
                        game=game
                    )
                )
            tiles.append(row)
        return tiles

    @classmethod
    def from_team(cls, team, game):
        return cls(
            id=team.id,
            player=PlayerPresenter.from_player(team.player),
            is_next=is_team_next(team, game),
            winner=team.winner,
            alive=team.alive,
            tiles=cls.make_tiles(team, game)
        )


class TilePresenter(namedtuple(
    'TilePresenter',
    ['x', 'y', 'name', 'is_empty', 'is_hit']
)):

    @classmethod
    def from_team(cls, x, y, team, game):
        is_empty = True
        for ship in team.ships.all():
            if (x, y) in ship.get_tiles():
                is_empty = False

        shots = Shot.objects.filter(game=game, defending_team=team)
        is_hit = (x, y) in [(shot.x, shot.y) for shot in shots]

        x_letter = chr(x + ord('A'))
        name = '{}{}'.format(x_letter, y)

        return cls(
            x=x,
            y=y,
            name=name,
            is_empty=is_empty,
            is_hit=is_hit
        )
