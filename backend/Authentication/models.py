from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

from Person.models import Person
from Event.models import Event
from University.models import University
from Sport.models import Sport
from Team.models import Team

class AdminRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)

class EventCoordinatorRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)

class UniversityCoordinatorRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=False, null=False)

class SportCoordinatorRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, blank=False, null=False)

class TeamCoordinatorRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, null=False)