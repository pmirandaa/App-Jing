from django.db import models
from django.contrib.auth.models import User

from Event.models import Event
from University.models import University

from django.core.validators import validate_email

class Person(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        blank=True, null=True
    )
    #event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[validate_email])
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    rut = models.CharField(max_length=13, unique=True)
    phone_number = models.CharField(max_length=20)
    emergency_phone_number = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(upload_to='person_avatars/', blank=True)
    pending_messages = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)

class PersonTemporaryCode(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    code = models.IntegerField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f'{self.person} - {self.code} -- {self.expiration_date}'
    
class Role(models.Model):
    roles= models.CharField(max_length=20)
    #permisos = models.
    def __str__(self):
        return f'{self.roles}'
    

class PER(models.Model):
    person= models.ForeignKey(Person, on_delete=models.CASCADE)
    event= models.ForeignKey(Event, on_delete=models.CASCADE)
    role= models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person} - {self.event} -- {self.role}'


