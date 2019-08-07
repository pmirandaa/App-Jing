from django.contrib import admin

# Register your models here.
from Team.models import Team
from Team.models import PlayerTeam

admin.site.register(Team)
admin.site.register(PlayerTeam)
