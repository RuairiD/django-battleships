from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from games.models import Team
from players.forms import UserForm
from players.forms import PlayerForm
from players.models import Player

class HomeView(View):

    template_name = 'base/home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated():
            player = Player.objects.get(user=request.user)
            teams = Team.objects.filter(player=player)
            context['games'] = [team.game for team in teams if team.alive]
        return render(request, self.template_name, context)


class SignupView(View):

    template_name = 'base/signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            user_form = UserForm()
            context = {
                'user_form': user_form
            }
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)

        if user_form.is_valid() and player_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            player = Player(user=user)
            player.save()

            login(request, user)

            return HttpResponseRedirect('/')
        else:
            context = {
                'user_form': user_form
            }
            messages.error(request, 'Something went wrong...')
            return render(request, self.template_name, context)


class LoginView(View):

    template_name = 'base/login.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        context = {}
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Your account is disabled.')
                return render(request, self.template_name, context)
        else:
            messages.error(request, 'Your username and/or password is incorrect.')
            return render(request, self.template_name, context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))
