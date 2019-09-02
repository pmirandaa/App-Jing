from django.db import models

# Create your models here.
from Person.models import Person


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
    sport_type = models.CharField(
        max_length=1, choices=SPORT_TYPE, default=TYPE_A)
    # rules = models.FileField(upload_to='uploads/reglamentos/')
    coordinator = models.ForeignKey(Person, on_delete=models.PROTECT)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(
            self.name,
            self.get_gender_display()
        )


class FinalSportPoints(models.Model):
    sport_type = models.CharField(max_length=1, choices=Sport.SPORT_TYPE)
    place = models.IntegerField()
    points = models.IntegerField()
