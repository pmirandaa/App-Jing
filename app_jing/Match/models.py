from django.db import models

from Event.models import Event
from Location.models import Location
from Team.models import Team
from Sport.models import Sport

# Create your models here.


class MatchTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    winner = models.BooleanField(default=False)
    comment = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return str(self.team)


class Match(models.Model):
    PENDING = 'MTB'  # Match to Be Played
    PLAYING = 'MIC'  # Match in Course
    PLAYED = 'MIF'  # Match is Finished

    MATCH_STATE = [
        (PENDING, 'Por jugar'),
        (PLAYING, 'En Curso'),
        (PLAYED, 'Jugado')
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    length = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    state = models.CharField(
        max_length=3, choices=MATCH_STATE, default=PENDING)
    teams = models.ManyToManyField(MatchTeam)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

    def __str__(self):
        match_teams = self.teams.all()
        teams = '-'.join([mt.team.university.short_name for mt in match_teams])
        return '{} ({})'.format(self.sport, teams)
