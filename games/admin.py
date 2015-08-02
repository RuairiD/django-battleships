from django.contrib import admin

from games.models import Game
from games.models import Ship
from games.models import Shot
from games.models import Team

class TeamInline(admin.StackedInline):
    model = Team

class ShipInline(admin.StackedInline):
    model = Ship

class ShotInline(admin.StackedInline):
    model = Shot

class GameAdmin(admin.ModelAdmin):
    inlines = [TeamInline, ShotInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [ShipInline]

admin.site.register(Game, GameAdmin)
admin.site.register(Ship)
admin.site.register(Shot)
admin.site.register(Team, TeamAdmin)
