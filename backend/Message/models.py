from django.db import models
from Event.models import Event
from Person.models import Person


class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reciever')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} --> {self.reciever} -- {self.subject}'
