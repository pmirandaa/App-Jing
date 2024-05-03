from django.db import models

# Create your models here.
from Person.models import Person
from Event.models import Event
from University.models import University
from simple_history.models import HistoricalRecords


class Sport(models.Model):
    MALES = 'MLE'
    FEMALE = 'FEM'
    MIX = 'MIX'

    SPORT_GENDER = [
        (MALES, 'Masculino'),
        (FEMALE, 'Femenino'),
        (MIX, 'Mixto')
    ]

    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'

    SPORT_TYPE = [
        (TYPE_A, 'Tipo A'),
        (TYPE_B, 'Tipo B'),
        (TYPE_C, 'Tipo C')
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=3, choices=SPORT_GENDER, default=MIX)
    history = HistoricalRecords()
    
    #sport_type = models.CharField(
     #   max_length=1, choices=SPORT_TYPE, default=TYPE_A)
    # rules = models.FileField(upload_to='uploads/reglamentos/')
    #coordinator = models.ForeignKey(Person, on_delete=models.PROTECT)
    #closed = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(
            self.name,
            self.get_gender_display()
        )

#class FinalSportPoints(models.Model):
 #   place = models.IntegerField()
  #  points = models.IntegerField()

class EventSport(models.Model): #deberia ir en el evento o en deportes?
    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'

    SPORT_TYPE = [
        (TYPE_A, 'Tipo A'),
        (TYPE_B, 'Tipo B'),
        (TYPE_C, 'Tipo C')
    ]

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE) #no puede ser unique porque pueden haber eventos con el mismo deporte
    closed= models.BooleanField(default=False)
    sport_type = models.CharField(
        max_length=1, choices=SPORT_TYPE, default=TYPE_A)

class SportCoordinator(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    coordinator= models.ForeignKey(Person, on_delete=models.CASCADE)

class SportStanding(models.Model):
    event_sport= models.ForeignKey(EventSport, on_delete=models.PROTECT)
    university=models.ForeignKey(University, on_delete=models.PROTECT)
    place = models.IntegerField()
    participated = models.BooleanField(default=False)
    history = HistoricalRecords()
