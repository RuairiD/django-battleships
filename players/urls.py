from django.conf.urls import include
from django.conf.urls import url

from players.views import PlayerProfileView

urlpatterns = [
    url(r'^(?P<username>.+)/$', PlayerProfileView.as_view(), name='player_profile'),
]