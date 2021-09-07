from django import template


register = template.Library()


@register.inclusion_tag('games/player_board.html')
def render_player_board(team, game_id):
    return {
            'team': team,
            'game_id': game_id,
            }


@register.inclusion_tag('games/opponent_board.html')
def render_opponent_board(team, game_id):
    return {
            'team': team,
            'game_id': game_id,
            }
