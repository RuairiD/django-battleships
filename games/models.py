from django.db import models

from players.models import Player

GAME_SIZE = 10
MAX_PLAYERS = 4


class Game(models.Model):
    """Model containing information on a single game of Battleships."""
    turn = models.IntegerField(default=0)

    def __str__(self):
        result = '{} -'.format(self.id)
        for team in self.teams.all():
            result += ' {}'.format(
                team.player.user.username
            )
        return result


class Team(models.Model):
    """Model containing Player information specific to a single Game."""
    player = models.ForeignKey(Player, related_name='teams',
            on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='teams',
            on_delete=models.CASCADE)
    last_turn = models.IntegerField(default=0)

    winner = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)

    def __str__(self):
        return 'Game {} - {} (last_turn={})'.format(
            self.game.id,
            self.player.user.username,
            self.last_turn
        )


class Shot(models.Model):
    """Model containing information of an attack."""
    game = models.ForeignKey(Game, related_name='shots',
            on_delete=models.CASCADE)
    attacking_team = models.ForeignKey(Team, related_name='attacking_shots',
            on_delete=models.CASCADE)
    defending_team = models.ForeignKey(Team, related_name='defending_shots',
            on_delete=models.CASCADE)

    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return 'Game {game_id} - '\
            '{attacking_team} attacked {defending_team} ({x}, {y})'.format(
                game_id=self.game.id,
                attacking_team=self.attacking_team.player.user.username,
                defending_team=self.defending_team.player.user.username,
                x=self.x,
                y=self.y
            )


class Ship(models.Model):
    """Model containing information of a single ship on the game board."""
    LENGTHS = [2, 3, 3, 4, 5]

    team = models.ForeignKey(Team, related_name='ships',
            on_delete=models.CASCADE)

    x = models.IntegerField()
    y = models.IntegerField()

    length = models.IntegerField()

    CARDINAL_DIRECTIONS = {
        'NORTH': 0,
        'SOUTH': 1,
        'EAST': 2,
        'WEST': 3
    }

    DIRECTION_CHOICES = (
        (CARDINAL_DIRECTIONS['NORTH'], 'North'),
        (CARDINAL_DIRECTIONS['SOUTH'], 'South'),
        (CARDINAL_DIRECTIONS['EAST'], 'East'),
        (CARDINAL_DIRECTIONS['WEST'], 'West'),
    )

    direction = models.IntegerField(choices=DIRECTION_CHOICES)

    def __str__(self):
        return 'Game {game_id} - {team}\'s {length}L '\
            'at ({x}, {y}) facing {direction}'.format(
                game_id=self.team.game.id,
                team=self.team.player.user.username,
                length=self.length,
                x=self.x,
                y=self.y,
                direction=self.DIRECTION_CHOICES[self.direction][1]
            )

    def get_tiles(self):
        """Returns a list of all tiles occupied by a ship."""
        tiles = []
        for i in range(0, self.length):
            if self.direction == Ship.CARDINAL_DIRECTIONS['NORTH']:
                tiles.append((self.x, self.y - i))
            elif self.direction == Ship.CARDINAL_DIRECTIONS['SOUTH']:
                tiles.append((self.x, self.y + i))
            elif self.direction == Ship.CARDINAL_DIRECTIONS['EAST']:
                tiles.append((self.x + i, self.y))
            elif self.direction == Ship.CARDINAL_DIRECTIONS['WEST']:
                tiles.append((self.x - i, self.y))
        return tiles
