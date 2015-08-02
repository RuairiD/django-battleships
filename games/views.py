from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from games.forms import AttackForm
from games.forms import CreateGameForm
from games.models import Game
from games.models import Ship
from games.models import Shot
from games.models import Team
from games.presentation import TeamPresenter
from games.util import is_team_next
from games.util import make_ships
from players.models import Player


class GameView(View):

    template_name = 'games/game.html'

    def get(self, request, game_id, *args, **kwargs):
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            raise Http404("Game does not exist")

        if request.user.is_authenticated():
            player = Player.objects.get(user=request.user)
            teams = game.team_set.all()

            player_team = None
            for team in teams:
                if team.player == player:
                    player_team = team
            if player_team is None:
                raise Http404("Player is not authorised.")

            team_presenters = [TeamPresenter.from_team(team, game) for team in teams]
            is_player_next = is_team_next(player_team, game)

            context = {
                'game_id': game_id,
                'player_team': TeamPresenter.from_team(player_team, game),
                'teams': team_presenters,
                'attack_form': AttackForm(),
                'is_player_next': is_player_next
            }
            return render(request, self.template_name, context)
        else:
            raise Http404("Player is not logged in.")


class CreateGameView(View):

    template_name = 'games/create_game.html'

    def get(self, request, *args, **kwargs):
        form = CreateGameForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            form = CreateGameForm(request.POST)
            if form.is_valid():
                opponent_username = form.cleaned_data['opponent_username']
                try:
                    opponent_user = User.objects.get(username=opponent_username)
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist! Are you sure the username is correct?')
                    context = {
                        'form': form
                    }
                    return render(request, self.template_name, context)

                user_player = Player.objects.get(user=request.user)
                opponent_player = Player.objects.get(user=opponent_user)

                # Create a game plus teams and ships for both players
                # Creation in Game -> Team -> Ships order is important to satisfy
                # ForeignKey dependencies.
                game = Game()
                game.save()
                user_team = Team(player=user_player, game=game, last_turn=-2)
                opponent_team = Team(player=opponent_player, game=game, last_turn=-1)
                user_team.save()
                opponent_team.save()

                user_ships = make_ships(user_team, Ship.LENGTHS)
                opponent_ships = make_ships(opponent_team, Ship.LENGTHS)
                for user_ship in user_ships:
                    user_ship.save()
                for opponent_ship in opponent_ships:
                    opponent_ship.save()

                return HttpResponseRedirect('/games/{id}'.format(id=game.id))
            else:
                messages.error(request, 'Invalid form.')
                context = {
                    'form': form
                }
                return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect('/login')


class AttackView(View):

    def post(self, request, *args, **kwargs):
        errors = []
        if request.user.is_authenticated():
            form = AttackForm(request.POST)
            if form.is_valid():
                game_id = form.cleaned_data['game_id']
                target_x = form.cleaned_data['target_x']
                target_y = form.cleaned_data['target_y']

                try:
                    game = Game.objects.get(pk=game_id)
                except Game.DoesNotExist:
                    raise Http404("Game does not exist.")

                player = Player.objects.get(user=request.user)

                # Verify the player is involved in this game
                teams = game.team_set.all()
                player_team = None
                for team in teams:
                    if team.player == player:
                        player_team = team
                if player_team is None:
                    raise Http404("Player is not authorised.")

                # Verify it is the player's turn to attack
                is_next = is_team_next(player_team, game)
                if not is_next:
                    messages.error(request, 'It\'s not your turn!')
                    return HttpResponseRedirect(reverse('game', args=[game_id]))

                other_team = list(filter(lambda team:team != player_team, teams))[0]

                # Verify shot hasn't already been attempted
                past_shots = Shot.objects.filter(
                    game=game,
                    attacking_team=player_team,
                    defending_team=other_team,
                    x=target_x,
                    y=target_y
                )

                if len(past_shots) > 0:
                    messages.error(request, 'You\'ve already shot there!')
                    return HttpResponseRedirect(reverse('game', args=[game_id]))

                shot = Shot(
                    game=game,
                    attacking_team=player_team,
                    defending_team=other_team,
                    x=target_x,
                    y=target_y
                )
                shot.save()

                player_team.last_turn = game.turn
                player_team.save()

                game.turn = game.turn + 1
                game.save()

                # Check for hit
                ship_tiles = set()
                for ship in other_team.ship_set.all():
                    ship_tiles.update(set(ship.get_tiles()))
                other_team_hit = (int(target_x), int(target_y)) in ship_tiles

                # Check for death
                shots = Shot.objects.filter(
                    game=game,
                    defending_team=other_team
                )
                shots = set([(shot.x, shot.y) for shot in shots])
                if len(shots.intersection(ship_tiles)) == len(ship_tiles):
                    messages.success(request, 'Shot successful!')
                    other_team.alive = False
                    other_team.save()
                other_team_defeated = not other_team.alive

                # Check for winner
                alive_teams = game.team_set.filter(alive=True)
                if len(alive_teams) == 1:
                    alive_teams[0].winner = True
                    alive_teams[0].save()

                if other_team_hit:
                    messages.success(request, 'Hit!')
                    if other_team_defeated:
                        messages.success(request, 'You defeated {name}!'.format(other_team.player.user.username))
                else:
                    messages.warning(request, 'Miss!')
                return HttpResponseRedirect(reverse('game', args=[game_id]))
            else:
                return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'You must be logged in to do that.')
            return HttpResponseRedirect('/login')
