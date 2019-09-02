from django.db import models
from django.contrib.auth.models import User

from Event.models import Event
from University.models import University


class Person(models.Model):
    user = models.ForeignKey(
        User, related_name='person', on_delete=models.CASCADE,
        blank=True, null=True
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    rut = models.CharField(max_length=13)
    phone_number = models.CharField(max_length=20)
    emergency_phone_number = models.CharField(max_length=20, null=True)
    is_admin = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    is_university_coordinator = models.BooleanField(default=False)
    is_sports_coordinator = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    has_avatar = models.BooleanField(default=False)
    pending_messages = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)


class PersonAvatar(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='person_avatars/')

    def __str__(self):
        return str(self.person)


class PersonTemporaryCode(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    code = models.IntegerField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f'{self.person} - {self.code} -- {self.expiration_date}'
