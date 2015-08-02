import random

from games.models import GAME_SIZE
from games.models import Ship

def are_ships_overlapping(ship1, ship2):
    for ship1_tile in ship1.get_tiles():
        for ship2_tile in ship2.get_tiles():
            if ship1_tile == ship2_tile:
                return True
    return False

def is_team_next(team, game):
    alive_teams = game.team_set.filter(alive=True)
    return (team == min(alive_teams, key=lambda team:team.last_turn))

def is_valid_ship_position(ship):
    y_inc = 0
    x_inc = 0

    if ship.direction == Ship.CARDINAL_DIRECTIONS['NORTH']:
        y_inc = -1
    elif ship.direction == Ship.CARDINAL_DIRECTIONS['SOUTH']:
        y_inc = 1
    elif ship.direction == Ship.CARDINAL_DIRECTIONS['EAST']:
        x_inc = 1
    elif ship.direction == Ship.CARDINAL_DIRECTIONS['WEST']:
        x_inc = -1

    for i in range(0, ship.length):
        if ship.x + i * x_inc < 0 or ship.x + i * x_inc >= GAME_SIZE:
            return False
        if ship.y + i * y_inc < 0 or ship.y + i * y_inc >= GAME_SIZE:
            return False

    return True

def make_ships(team, lengths):
    ships = []
    for length in lengths:
        overlapping = False
        valid_position = False
        x = None
        y = None
        direction = None

        while overlapping or not valid_position:
            x = random.randrange(0, GAME_SIZE)
            y = random.randrange(0, GAME_SIZE)
            direction = Ship.CARDINAL_DIRECTIONS[random.choice(list(Ship.CARDINAL_DIRECTIONS.keys()))]

            ship = Ship(
                team=team,
                x=x,
                y=y,
                length=length,
                direction=direction
            )

            valid_position = is_valid_ship_position(ship)
            overlapping = False
            for existing_ship in ships:
                overlapping = overlapping or are_ships_overlapping(ship, existing_ship)

        ships.append(ship)

    return ships