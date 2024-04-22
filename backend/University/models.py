from django.db import models

from Event.models import Event


class University(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    #overall_score = models.IntegerField(default=0)
    logo = models.ImageField(
        upload_to='university/logo/', blank=True, null=True)
    map = models.ImageField(upload_to='university/map/', blank=True, null=True)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name} - {self.city}'


class UniversityEvent(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)

class EventStanding(models.Model):
    pass

