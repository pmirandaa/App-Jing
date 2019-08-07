from django.contrib import admin

# Register your models here.
from Match.models import Match
from Match.models import MatchTeam

admin.site.register(Match)
admin.site.register(MatchTeam)
