from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    overall_score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.city}'


class UniversityLogo(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='university_logo/')

    def __str__(self):
        return str(self.university)