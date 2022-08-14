from django.contrib import admin

from Match.models import Match
from Match.models import MatchTeam

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_id', 'location_id', 'date', 'sport_id', 'scores', 'winners', 'played', 'closed')
    search_fields = ('event__name', 'event__year', 'sport__name', 'team__university__short_name', 'team__coordinator__name')

    def teams(self, obj):
        return '-'.join(sorted([str(mt.team.university_id) for mt in obj.match_teams.all()]))
    
    def scores(self, obj):
        scrs = sorted([(mt.team.university_id, mt.score) for mt in obj.match_teams.all()])
        return ', '.join([f'({u}: {s})' for u, s in scrs])
    
    def winners(self, obj):
        return ', '.join(sorted([str(mt.team.university_id) for mt in obj.match_teams.filter(is_winner=True)]))

class MatchTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_id', 'university_id', 'match_id', 'event', 'sport_id', 'score', 'has_comment', 'is_winner', 'attended')
    search_fields = ('team__university__short_name', 'team__coordinator__name', 'score')
    autocomplete_fields = ['match', 'team']

    def has_comment(self, obj):
        return len(obj.comment) > 0

    def event(self, obj):
        event = obj.match.event
        return f"{event.id}: {event.name}"

    def sport_id(self, obj):
        return obj.match.sport_id

    def university_id(self, obj):
        return obj.team.university_id
    
    has_comment.boolean = True

admin.site.register(Match, MatchAdmin)
admin.site.register(MatchTeam, MatchTeamAdmin)
