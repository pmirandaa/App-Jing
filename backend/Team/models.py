from django.db import models

from Person.models import Person
from University.models import University
from Sport.models import Sport
from Event.models import Event

from simple_history.models import HistoricalRecords
# Create your models here.


class Team(models.Model):
    coordinator = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    place = models.PositiveIntegerField(default=0)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {} {}'.format(
            self.sport.name,
            self.sport.get_gender_display(),
            self.university.short_name
        )


class PlayerTeam(models.Model):
    player = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{} ({})'.format(self.player.name, self.team)
