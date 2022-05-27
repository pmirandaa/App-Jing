from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='events/')

    def __str__(self):
        return f'{self.name} -- {self.year}'
