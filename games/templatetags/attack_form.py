from django import template


register = template.Library()


@register.inclusion_tag('games/attack_form.html')
def render_attack_form(attack_form, game_id):
    return {
        'attack_form': attack_form,
        'game_id': game_id
    }
