from django.conf.urls import include
from django.conf.urls import url

from games.views import AttackView
from games.views import CreateGameView
from games.views import GameView

urlpatterns = [
    url(r'^attack/$', AttackView.as_view(), name='attack'),
    url(r'^create_game/$', CreateGameView.as_view(), name='create_game'),
    url(r'^(?P<game_id>.+)/$', GameView.as_view(), name='game'),
]