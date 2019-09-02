from django.contrib import admin

from Match.models import Match
from Match.models import MatchTeam

class MatchAdmin(admin.ModelAdmin):
    list_display = ('event', 'location', 'date', 'sport', 'team', 'closed')
    search_fields = ('event__name', 'event__year', 'sport__name', 'team__university__short_name', 'team__coordinator__name')

    def team(self, obj):
        return ' - '.join([mt.team.university.short_name for mt in obj.teams.all()])


class MatchTeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'score', 'Winner', 'has_comment')
    search_fields = ('team__university__short_name', 'team__coordinator__name', 'score')

    def has_comment(self, obj):
        return len(obj.comment) > 0

    def Winner(self, obj):
        return str(obj.team)
    
    has_comment.boolean = True

admin.site.register(Match, MatchAdmin)
admin.site.register(MatchTeam, MatchTeamAdmin)
