from django.db import models

from University.models import University


class Location(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
