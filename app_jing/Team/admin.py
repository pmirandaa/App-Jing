from django.contrib import admin

from Team.models import Team
from Team.models import PlayerTeam


class TeamAdmin(admin.ModelAdmin):
    list_display = ('event', 'Sport', 'Coordinator')
    search_fields = ('event__name', 'event__year', 'sport__name', 'coordinator__name', 'university__short_name')

    def Sport(self, obj):
        return f'{obj.university.short_name} - {obj.sport}'

    def Coordinator(self, obj):
        return obj.coordinator or '-'


class TeamPlayerAdmin(admin.ModelAdmin):
    list_display = ('team', 'player')
    search_fields = ('team__sport__name', 'player__name', 'team__university__name')


admin.site.register(Team, TeamAdmin)
admin.site.register(PlayerTeam, TeamPlayerAdmin)
