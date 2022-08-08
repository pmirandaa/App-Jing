from django.db import models

from Event.models import Event
from Sport.models import Sport


class EventPlacement(models.Model):
    event = models.ForeignKey(Event, related_name="placements", on_delete=models.CASCADE)
    university = models.ForeignKey(
        'University.University', null=True, on_delete=models.SET_NULL)
    points = models.PositiveIntegerField(default=0)
    place = models.PositiveIntegerField(default=0)


class SportPlacement(models.Model):
    sport = models.ForeignKey(Sport, related_name="placements", on_delete=models.CASCADE)
    university = models.ForeignKey(
        'University.University', null=True, on_delete=models.SET_NULL)
    place = models.PositiveIntegerField(default=0)
    participated = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.place}, Sport: {self.sport_id}, Univ: {self.university_id}, {self.participated}"