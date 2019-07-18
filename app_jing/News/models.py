from django.db import models

from Event.models import Event
from Person.models import Person


class NewsCategory(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=15)
    btn_class = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=250)
    short_story = models.TextField()
    date = models.DateTimeField()
    publisher = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True)
    body = models.TextField()
    category = models.ForeignKey(NewsCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
    picture = models.ImageField(upload_to='news/', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.date} -- {self.publisher}'
